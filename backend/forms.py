from django import forms

from .models import CurrencyRate


class ConversionForm(forms.Form):
    supported_currencies = CurrencyRate.objects.values_list('currency', flat=True)
    CURRENCIES_CHOICES = list(zip(supported_currencies, supported_currencies))

    from_currency = forms.ModelChoiceField(queryset=CurrencyRate.objects.all())
    to_currency = forms.ModelChoiceField(queryset=CurrencyRate.objects.all())
    amount = forms.DecimalField(max_digits=10, decimal_places=4)

    def clean(self):
        cleaned_data = super().clean()
        from_currency = cleaned_data.get("from_currency")
        to_currency = cleaned_data.get("to_currency")
        amount = cleaned_data.get("amount")

        if from_currency == to_currency:
            raise forms.ValidationError("From and to currency should be different")

        if amount <= 0:
            raise forms.ValidationError("Amount should be greater than 0")

        return cleaned_data
