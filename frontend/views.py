from decimal import Decimal

from django.shortcuts import render, redirect

from backend.forms import ConversionForm
from backend.models import CurrencyRate, Conversion
from backend.views import UserCreateAPIView, LoginView, LogoutView


def conversion_form(request):
    if request.method == 'GET':
        conversion = ConversionForm()
        return render(request, 'conversion_form.html', {'form': conversion})
    else:
        conversion_form = ConversionForm(request.POST)
        if conversion_form.is_valid():
            from_currency = conversion_form.cleaned_data['from_currency'].currency
            to_currency = conversion_form.cleaned_data['to_currency'].currency
            amount = conversion_form.cleaned_data['amount']

            from_rate = CurrencyRate.objects.get(currency=from_currency).rate
            to_rate = CurrencyRate.objects.get(currency=to_currency).rate
            # Convert rate to Decimal to avoid JSON serialization error
            from_rate = Decimal(str(from_rate))
            to_rate = Decimal(str(to_rate))

            converted_amount = amount * (to_rate / from_rate).quantize(Decimal('0.0001'))

            converted = Conversion.objects.create(
                from_currency=from_currency,
                to_currency=to_currency,
                amount=amount,
                converted_amount=converted_amount
            )
            converted.save()
            return render(request, 'conversion_form.html', {'form': conversion_form,
                                                            'converted_amount': converted_amount,
                                                            'currency_code': to_currency})
        else:
            return render(request, 'conversion_form.html', {'form': conversion_form})


def login_form(request):
    if request.method == 'GET':
        return render(request, 'login_form.html')
    elif request.method == 'POST':
        data = {
            "username": request.POST.get('username'),
            "password": request.POST.get('password')
        }
        user = LoginView()
        request.data = data
        response_login = LoginView.post(user, request)

        if response_login.status_code == 200:
            return redirect('conversion_form')
        else:
            message = "Username ou senha inválidos!"
            return render(request, 'login_form.html', {'messages': [message]})


def register_form(request):
    if request.method == 'GET':
        return render(request, 'create_user.html')
    elif request.method == 'POST':
        data = {
            "username": request.POST.get('username'),
            "password": request.POST.get('password1'),
            "email": request.POST.get('email'),
            "first_name": request.POST.get('first_name'),
            "last_name": request.POST.get('last_name')
        }

        user = UserCreateAPIView()
        user.data = data
        response = UserCreateAPIView.post(user, user)

        if response.status_code != 201:
            return render(request, 'create_user.html', {'messages': ["Dados inválidos!"]})
        return render(request, 'login_form.html', {'messages': ["Usuário criado com sucesso!"]})


def logout(request):
    if request.method == 'GET':
        return render(request, 'logout.html')
    elif request.method == 'POST':
        data = {
            "username": request.POST.get('username'),
            "password": request.POST.get('password')
        }
        user_logout = LogoutView()
        user_logout.data = data
        response_logout = LogoutView.post(user_logout, request)
        if response_logout.status_code == 200:
            return render(request, 'login_form.html', {'messages': ["Usuário deslogado com sucesso!"]})
        elif response_logout.status_code == 400:
            return render(request, 'logout.html', {'messages': ["Usuário não logado!"]})
