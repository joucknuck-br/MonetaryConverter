from decimal import Decimal

from django.core.management import call_command
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView

from .models import CurrencyRate
from .forms import ConversionForm


class CurrencyRateListView(ListView):
    """
    View to list currency rates
    """

    model = CurrencyRate
    queryset = CurrencyRate.objects.all().order_by("currency")

    def get(self, request, *args, **kwargs):
        rates_list = list(self.queryset.values('currency', 'rate'))
        return JsonResponse({'rates': rates_list})


class CurrencyRateDetailView(DetailView):
    """
    View to show currency rate detail
    """

    model = CurrencyRate

    def get_object(self, queryset=None):
        currency_code = self.kwargs.get("currency_code")
        return CurrencyRate.objects.get(currency=currency_code)


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

        from_rate = CurrencyRate.objects.get(currency=from_currency.currency).rate
        to_rate = CurrencyRate.objects.get(currency=to_currency.currency).rate
        from_rate = Decimal(str(from_rate))
        to_rate = Decimal(str(to_rate))

        converted_amount = amount * (to_rate / from_rate)

        return self.render_to_response({
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "converted_amount": converted_amount,
        })

    def form_invalid(self, form):
        return self.render_to_response({"form": form})


def trigger_currency_update(request):
    call_command('update_currencies')
    return JsonResponse({"status": "success"})
