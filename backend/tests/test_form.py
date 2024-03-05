import django
django.setup()

from django.test import TestCase

from backend.forms import ConversionForm


class ConversionFormTests(TestCase):

    def test_valid_data(self):
        form = ConversionForm(data={
            'from_currency': 'USD',
            'to_currency': 'BRL',
            'amount': '100.00'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = ConversionForm(data={
            'from_currency': 'INVALID',
            'to_currency': 'INVALID',
            'amount': 'abc'
        })
        self.assertFalse(form.is_valid())