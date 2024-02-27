from django.urls import path
from .views import CurrencyRateListView, CurrencyRateDetailView, ConversionView

urlpatterns = [
    path('rates/', CurrencyRateListView.as_view(), name='currency-rates'),
    path('rates/<str:currency_code>/', CurrencyRateDetailView.as_view(), name='currency-rate-detail'),
    path('convert/', ConversionView.as_view(), name='conversion'),
]