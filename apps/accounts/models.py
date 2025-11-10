from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Account(models.Model):
    class Currency(models.TextChoices):
        NTD = "NT$", "NTD"
        USD = "US$", "USD"
        EUR = "€", "EUR"
        GBP = "£", "GBP"

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
        from apps.records.models import Record
        from django.db.models import Sum

        record_sum = Record.objects.filter(
            user=self.user, type="Expense", account=self
        ).aggregate(Sum("amount"))
        return record_sum["amount__sum"] or 0

    @property
    def total_income(self):
        from apps.records.models import Record
        from django.db.models import Sum

        record_sum = Record.objects.filter(
            user=self.user, type="Income", account=self
        ).aggregate(Sum("amount"))
        return record_sum["amount__sum"] or 0

    def cal_cur_amount(self):
        cal_amount = self.init_amount - self.total_expense + self.total_income
        self.cur_amount = cal_amount
        self.save()

    class Meta:
        indexes = [models.Index(fields=["user", "created_at"])]
