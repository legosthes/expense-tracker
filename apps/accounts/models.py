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
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    @property
    def total_expense(self):
        pass

    @property
    def total_income(self):
        pass
