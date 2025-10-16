from apps.records.models import Record
from apps.accounts.models import Account
from django.forms import ModelForm, Select, NumberInput, Textarea, ModelChoiceField


class RecordForm(ModelForm):
    account = ModelChoiceField(
        queryset=None,
        widget=Select(attrs={"class": "select"}),
    )

    class Meta:
        model = Record
        fields = ["account", "amount", "type", "category", "notes"]
        labels = {
            "account": "Account",
            "amount": "Amount",
            "type": "Type",
            "category": "Category",
            "notes": "Notes",
        }
        widgets = {
            "amount": NumberInput(attrs={"step": "0.01", "class": "input"}),
            "type": Select(attrs={"class": "select"}),
            "category": Select(attrs={"class": "select"}),
            "notes": Textarea(attrs={"rows": 5, "class": "textarea"}),
        }
