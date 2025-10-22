from apps.accounts.models import Account
from django.forms import ModelForm, TextInput, Select, NumberInput


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ["name", "init_amount", "currency"]
        labels = {
            "name": "Account Name",
            "init_amount": "Initial Amount",
            "currency": "Currency",
        }
        widgets = {
            "name": TextInput(attrs={"class": "input w-full"}),
            "init_amount": NumberInput(attrs={"step": "0.01", "class": "input w-full"}),
            "currency": Select(attrs={"class": "select w-full"}),
        }
