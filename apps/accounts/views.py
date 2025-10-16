from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Account
from apps.records.models import Record
from apps.accounts.forms import AccountForm
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Sum


# Create your views here.
@login_required
def accounts(request):
    accounts = Account.objects.filter(user_id=request.user)
    records = Record.objects.filter(user_id=request.user)
    total_sums = (
        accounts.values("currency").annotate(sum=Sum("init_amount")).order_by("-sum")
    )
    if request.POST:
        form = AccountForm(request.POST)
        account = form.save(commit=False)
        account.user = request.user
        account.save()
        return redirect("accounts:accounts")
    else:
        return render(
            request,
            "pages/accounts.html",
            {
                "accounts": accounts,
                "sums": total_sums,
                "records": records,
            },
        )


@login_required
def new_account(request):
    form = AccountForm()
    return render(request, "pages/new_account.html", {"form": form})


@login_required
def edit_account(request, user_id, account_id):
    account = Account.objects.get(pk=account_id, user=user_id)
    form = AccountForm(instance=account)
    return render(
        request, "pages/edit_account.html", {"form": form, "account": account}
    )


@login_required
@require_POST
def update_account(request, user_id, account_id):
    account = Account.objects.get(pk=account_id, user=user_id)
    form = AccountForm(request.POST, instance=account)
    form.save()
    return redirect("accounts:accounts")


@login_required
@require_POST
def delete_account(request, user_id, account_id):
    account = Account.objects.get(pk=account_id, user=user_id)
    account.delete()
    response = HttpResponse(status=200)
    response["HX-Redirect"] = reverse("accounts:accounts")
    return response
