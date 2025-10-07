from django.db import models
from django.contrib.auth.models import User
from apps.accounts.models import Account


# Create your models here.
class Record(models.Model):
    class RecordType(models.TextChoices):
        Expense = "Expense", "Expense"
        Income = "Income", "Income"
        Transfer = "Transfer", "Transfer"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    type = models.CharField(max_length=20, choices=RecordType)
