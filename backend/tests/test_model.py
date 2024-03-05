import django
django.setup()

from django.test import TestCase

from backend.models import CurrencyRate, Conversion


class CurrencyRateTests(TestCase):

    def test_str_representation(self):
        currency_rate = CurrencyRate(currency='USD', rate='1.0000')
        self.assertEqual(str(currency_rate), 'USD: 1.0000')

    def test_create_currency_rate(self):
        currency_rate = CurrencyRate.objects.create(currency='USD', rate='1.0000')
        self.assertEqual(currency_rate.currency, 'USD')
        self.assertEqual(currency_rate.rate, '1.0000')


class ConversionTests(TestCase):

    def test_str_representation(self):
        conversion = Conversion(from_currency='USD', to_currency='BRL', amount='100.00', converted_amount='500.00')
        self.assertEqual(str(conversion), 'USD to BRL: 100.00 (500.00)')

    def test_create_conversion(self):
        conversion = Conversion.objects.create(from_currency='USD', to_currency='BRL', amount='100.00', converted_amount='500.00')
        self.assertEqual(conversion.from_currency, 'USD')
        self.assertEqual(conversion.to_currency, 'BRL')
        self.assertEqual(conversion.amount, '100.00')
        self.assertEqual(conversion.converted_amount, '500.00')