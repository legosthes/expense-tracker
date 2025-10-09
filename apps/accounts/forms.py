from apps.accounts.models import Account
from django.forms import ModelForm, TextInput, Select, DecimalField


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
            "name": TextInput,
            "init_amount": DecimalField,
            "currency": Select,
        }
