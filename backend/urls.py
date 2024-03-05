from django.urls import path

from .views import post_conversion, trigger_currency_update, get_all, get_object, UserCreateAPIView, \
    get_all_conversions, LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserCreateAPIView.as_view(), name='user-create'),
    path('rates/', get_all, name='currency-rates'),
    path('rates/<str:currency_code>/', get_object, name='currency-rate-detail'),
    path('convert/', post_conversion, name='convert'),
    path('conversions/', get_all_conversions, name='conversions'),
    path('update-rates/', trigger_currency_update, name='update-rates'),
]
