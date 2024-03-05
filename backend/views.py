from decimal import Decimal

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
from requests import get
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CurrencyRate, Conversion
from .serializers import UserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, req, *args, **kwargs):
        username = req.data.get('username')
        password = req.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(req, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({
                "message": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request):
        try:
            logout(request)
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Error " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserCreateAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        # Check if the user already exists
        if User.objects.filter(username=request.data['username']):
            return Response({
                "message": "User already exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=request.data['email']):
            return Response({
                "message": "Email is already in use"
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get request
@api_view(['GET'])
def get_all(request):
    rates_list = list(CurrencyRate.objects.all().values('currency', 'rate'))
    # Convert rate to Decimal to avoid JSON serialization error
    rates_list = [{'currency': rate['currency'], 'rate': Decimal(str(rate['rate']))} for rate in rates_list]

    return JsonResponse({
        'rates': rates_list
    })


# Get request
@api_view(['GET'])
def get_object(request, currency_code):
    if not CurrencyRate.objects.filter(currency=currency_code):
        return JsonResponse({
            "message": "Currency not found"
        }, status=status.HTTP_404_NOT_FOUND)
    currency_obj = CurrencyRate.objects.get(currency=currency_code)

    return JsonResponse({
        'currency': currency_obj.currency,
        'rate': Decimal(str(currency_obj.rate))
    })


# Post request
@api_view(['POST'])
def post_conversion(request):
    if not request.data:
        return JsonResponse({
            "message": "No data provided"
        })
    from_currency = request.data.get("from_currency")
    to_currency = request.data.get("to_currency")
    if not CurrencyRate.objects.filter(currency=from_currency) or not CurrencyRate.objects.filter(currency=to_currency):
        return JsonResponse({
            "message": "Currency not found"
        }, status=status.HTTP_404_NOT_FOUND)

    amount = Decimal(str(request.data.get("amount")))
    if amount <= 0 or amount.is_nan():
        return JsonResponse({
            "message": "Invalid amount"
        }, status=status.HTTP_400_BAD_REQUEST)

    from_rate = CurrencyRate.objects.get(currency=from_currency).rate
    to_rate = CurrencyRate.objects.get(currency=to_currency).rate
    # Convert rate to Decimal to avoid JSON serialization error
    from_rate = Decimal(str(from_rate))
    to_rate = Decimal(str(to_rate))

    converted_amount = amount * (to_rate / from_rate).quantize(Decimal('0.0001'))

    conversion = Conversion.objects.create(
        from_currency=from_currency,
        to_currency=to_currency,
        amount=amount,
        converted_amount=converted_amount
    )
    conversion.save()

    return JsonResponse({
        "from_currency": conversion.from_currency,
        "to_currency": conversion.to_currency,
        "amount": conversion.amount,
        "converted_amount": conversion.converted_amount,
        "created_at": conversion.created_at,
    })


# Get request
@api_view(['GET'])
def get_all_conversions(request):
    conversions_list = list(
        Conversion.objects.all().values('from_currency', 'to_currency', 'amount', 'converted_amount', 'created_at'))
    # Convert rate to Decimal to avoid JSON serialization error
    conversions_list = [
        {
            'from_currency': conversion['from_currency'],
            'to_currency': conversion['to_currency'],
            'amount': Decimal(str(conversion['amount'])),
            'converted_amount': Decimal(str(conversion['converted_amount'])),
            'created_at': conversion['created_at']
        }
        for conversion in conversions_list
    ]

    return JsonResponse({
        'conversions': conversions_list
    })


# Get request
def trigger_currency_update(request):
    api_url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = get(api_url)

    if response.status_code == 200:
        data = response.json()["rates"]
        for currency_code, rate in data.items():
            if currency_code in ["USD", "BRL", "EUR"]:
                CurrencyRate.objects.update_or_create(
                    currency=currency_code,
                    defaults={'rate': rate},
                )
    else:
        return JsonResponse({
            "status": "error",
            "message": "Failed to update standard currencies"
        })

    crypto_api_url = "https://min-api.cryptocompare.com/data/pricemulti"
    api_key = "f3dfbec9bc987624d350f9ef5b8b0393c1c235924ef4c331fd6442cca781638b"
    currencies = "BTC,ETH"
    base_currency = "USD"

    payload = {'fsyms': currencies, 'tsyms': base_currency, 'api_key': api_key}
    response = get(crypto_api_url, params=payload)

    if response.status_code == 200:
        data = response.json()
        for currency_code, rates in data.items():
            CurrencyRate.objects.update_or_create(
                currency=currency_code,
                defaults={'rate': rates[base_currency]},
            )
    else:
        return JsonResponse({
            "status": "error",
            "message": "Failed to update crypto currencies"
        })

    currencies_list = list(CurrencyRate.objects.all().values('currency', 'rate'))
    # Convert rate to Decimal to avoid JSON serialization error
    currencies_list = [{'currency': rate['currency'], 'rate': Decimal(str(rate['rate']))} for rate in currencies_list]

    return JsonResponse({
        "status": "success",
        "message": "Currencies updated successfully",
        "data": currencies_list,
    })
