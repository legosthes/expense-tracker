from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Account
from apps.accounts.forms import AccountForm


# Create your views here.
@login_required
def accounts(request, user_id):
    accounts = Account.objects.filter(user_id=user_id)
    if request.POST:
        form = AccountForm(request.POST)
        account = form.save(commit=False)
        account.user_id = user_id
        account.save()
        return redirect("accounts:accounts", user_id)
    else:
        return render(request, "pages/accounts.html", {"accounts": accounts})


@login_required
def new_account(request):
    form = AccountForm()
    return render(request, "pages/new_account.html", {"form": form})
