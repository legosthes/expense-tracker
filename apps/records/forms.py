from apps.records.models import Record
from apps.accounts.models import Account
from django.forms import ModelForm, Select, NumberInput, Textarea, ModelChoiceField


class RecordForm(ModelForm):
    account = ModelChoiceField(
        queryset=None,
        widget=Select(attrs={"class": "select w-full"}),
    )

    def __init__(self, *args, user=None, **kwargs):
        # set up the form first, including the fields
        super().__init__(*args, **kwargs)

        if user:
            self.fields["account"].queryset = Account.objects.filter(user=user)

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
            "amount": NumberInput(attrs={"step": "0.01", "class": "input w-full"}),
            "type": Select(attrs={"class": "select w-full"}),
            "category": Select(attrs={"class": "select w-full"}),
            "notes": Textarea(attrs={"rows": 3, "class": "textarea w-full"}),
        }
