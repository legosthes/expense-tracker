from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Account
from apps.accounts.forms import AccountForm


# Create your views here.
@login_required
def accounts(request, id):
    accounts = Account.objects.filter(user_id=id)
    return render(request, "pages/accounts.html", {"accounts": accounts})


@login_required
def new_account(request):
    form = AccountForm
    pass
