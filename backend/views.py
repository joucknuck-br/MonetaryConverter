from decimal import Decimal

from django.core.management import call_command
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CurrencyRate, Conversion
from .serializers import UserSerializer


class UserCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
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
    amount = request.data.get("amount")

    from_rate = CurrencyRate.objects.get(currency=from_currency).rate
    to_rate = CurrencyRate.objects.get(currency=to_currency).rate
    # Convert rate to Decimal to avoid JSON serialization error
    from_rate = Decimal(str(from_rate))
    to_rate = Decimal(str(to_rate))

    converted_amount = amount * (to_rate / from_rate)

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
    conversions_list = list(Conversion.objects.all().values('from_currency', 'to_currency', 'amount', 'converted_amount', 'created_at'))
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
@api_view(['GET'])
def trigger_currency_update(request):
    if call_command('update_currencies'):
        return JsonResponse({
            "message": "Currency rates updated successfully"
        })
    else:
        return JsonResponse({
            "message": "Failed to update currency rates"
        })
