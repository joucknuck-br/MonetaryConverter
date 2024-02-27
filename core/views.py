from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView

from .models import CurrencyRate
from .forms import ConversionForm


class CurrencyRateListView(ListView):
    """
    View to list currency rates
    """

    model = CurrencyRate
    queryset = CurrencyRate.objects.all().order_by("currency")


class CurrencyRateDetailView(DetailView):
    """
    View to show currency rate detail
    """

    model = CurrencyRate


class ConversionView(FormView):
    """
    View to convert currency
    """

    form_class = ConversionForm
    template_name = "conversion_form.html"


def form_valid(self, form):
    from_currency = form.cleaned_data["from_currency"]
    to_currency = form.cleaned_data["to_currency"]
    amount = form.cleaned_data["amount"]

    from_rate = CurrencyRate.objects.get(currency=from_currency).rate
    to_rate = CurrencyRate.objects.get(currency=to_currency).rate

    converted_amount = amount * (to_rate / from_rate)

    return self.render_to_response({
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount,
        "converted_amount": converted_amount,
    })
