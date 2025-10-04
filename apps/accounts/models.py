from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Account(models.Model):
    class Currency(models.TextChoices):
        NTD = "NTD", "New Taiwan Dollar"
        USD = "USD", "United States Dollar"
        EUR = "EUR", "Euro"
        GBP = "GBP", "Great British Pound"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=False, null=False)
    init_amount = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    currency = models.CharField(max_length=30, choices=Currency, default=Currency.NTD)
