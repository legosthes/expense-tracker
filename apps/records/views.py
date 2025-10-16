from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Account
from apps.records.forms import RecordForm


@login_required
def new_record(request, user_id):
    form = RecordForm()
    form.fields["account"].queryset = Account.objects.filter(user_id=request.user)
    return render(request, "pages/new_record.html", {"form": form})
