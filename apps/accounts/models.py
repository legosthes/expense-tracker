from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Account(models.Model):
    class Currency(models.TextChoices):
        NTD = "NT$", "New Taiwan Dollar"
        USD = "US$", "United States Dollar"
        EUR = "€", "Euro"
        GBP = "£", "Great British Pound"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=30,
        blank=False,
        default="UserAccount",
    )
    init_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    cur_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    currency = models.CharField(max_length=30, choices=Currency, default=Currency.NTD)

    def __str__(self):
        return self.name
