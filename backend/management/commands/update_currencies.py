from django.core.management import BaseCommand
from requests import get

from ...models import CurrencyRate


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = get(api_url)

        if response.status_code == 200:
            data = response.json()["rates"]
            for currency_code, rate in data.items():
                obj, created = CurrencyRate.objects.update_or_create(
                    currency=currency_code,
                    defaults={'rate': rate},
                )
                if created:
                    print(f"Added: {currency_code} - {rate}")
                else:
                    print(f"Updated: {currency_code} - {rate}")
        else:
            print("Error fetching data from API")
