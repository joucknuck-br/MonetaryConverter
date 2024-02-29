from django.http import HttpRequest
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from backend.forms import ConversionForm
from backend.views import UserCreateAPIView
from utils.authentication import LoginView


@api_view(['GET', 'POST'])
def conversion_form(request):
    if request.method == 'GET':
        conversion = ConversionForm()
        return render(conversion, 'conversion_form.html')
    else:
        redirect('post_conversion')


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
        request_login = HttpRequest()
        request_login.data = response_login.data
        response_login.method = 'POST'
        if response_login.status_code == 200:
            return conversion_form(request_login)
        else:
            message = "Invalid username or password"
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
        UserCreateAPIView.post(user, user)
        return render(request, 'login_form.html')


@api_view(['GET', 'POST'])
def logout(request):
    return render(request, 'login_form.html')
