from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Account
from apps.records.models import Record
from apps.accounts.forms import AccountForm
from apps.records.forms import RecordForm
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Sum


# Create your views here.
@login_required
def accounts(request):
    accounts = Account.objects.filter(user_id=request.user).order_by("created_at")
    for account in accounts:
        account.cal_cur_amount()

    records = Record.objects.filter(user_id=request.user).order_by("-created_at")
    total_sums = (
        accounts.values("currency").annotate(sum=Sum("cur_amount")).order_by("-sum")
    )
    if request.POST:
        if request.POST["_method"] == "account":
            form = AccountForm(request.POST)
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect("accounts:accounts")
        if request.POST["_method"] == "record":
            form = RecordForm(request.POST, user=request.user)
            if form.is_valid():
                record = form.save(commit=False)
                record.user = request.user
                record.save()
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
def edit_account(request, account_id):
    account = Account.objects.get(pk=account_id, user=request.user)
    form = AccountForm(instance=account)
    return render(
        request, "pages/edit_account.html", {"form": form, "account": account}
    )


@login_required
@require_POST
def update_account(request, account_id):
    account = Account.objects.get(pk=account_id, user=request.user)
    form = AccountForm(request.POST, instance=account)
    form.save()
    return redirect("accounts:accounts")


@login_required
@require_POST
def delete_account(request, account_id):
    account = Account.objects.get(pk=account_id, user=request.user)
    account.delete()
    response = HttpResponse(status=200)
    response["HX-Redirect"] = reverse("accounts:accounts")
    return response
