from django.db import models


class CurrencyRate(models.Model):
    """
    Model to store currency rates
    """
    currency = models.CharField(max_length=3, unique=True)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.currency}: {self.rate}"


class Conversion(models.Model):
    """
    Model to store currency conversions
    """

    from_currency = models.CharField(max_length=3)
    to_currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    converted_amount = models.DecimalField(max_digits=10, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_currency} -> {self.to_currency}: {self.amount} ({self.converted_amount})"
