from django.db import models
from django.contrib.auth.models import User
from apps.accounts.models import Account


# Create your models here.
class Record(models.Model):
    class RecordType(models.TextChoices):
        Expense = "Expense", "Expense"
        Income = "Income", "Income"

    class ExpenseCategory(models.TextChoices):
        Restaurants = "Restaurants", "Restaurants"
        Transportation = "Transportation", "Transportation"
        Groceries = "Groceries", "Groceries"
        Shopping = "Shopping", "Shopping"
        Housing = "Housing", "Housing"
        Life_Entertainment = "Life & Entertainment", "Life & Entertainment"
        Income = "Income", "Income"
        Others = "Others", "Others"

    class IncomeCategory(models.TextChoices):
        Salary = "Salary", "Salary"
        Dividends = "Dividends", "Dividends"
        Interests = "Interests", "Interests"
        Gifts = "Gifts", "Gifts"
        Others = "Others", "Others"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=False,
        null=False,
    )
    type = models.CharField(max_length=20, choices=RecordType)
    category = models.CharField(max_length=20, choices=ExpenseCategory, null=False)
    notes = models.TextField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
