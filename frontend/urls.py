from django.urls import path

from frontend.views import conversion_form, register_form, logout, login_form

urlpatterns = [
    path('login_form/', login_form, name='login_form'),
    path('register_form/', register_form, name='register_form'),
    path('logout/', logout, name='logout_form'),
    path('conversion_form/', conversion_form, name='conversion_form'),
]