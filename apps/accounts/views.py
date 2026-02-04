from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Account
from apps.records.models import Record
from apps.accounts.forms import AccountForm
from apps.records.forms import RecordForm
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Sum, Case, When, DecimalField
from apps.ai.langchain import analyze_records
from datetime import timedelta
from datetime import datetime
from django.db.models import F


# Create your views here.
@login_required
def accounts(request):
    categories = Record.ExpenseCategory
    accounts = Account.objects.filter(user_id=request.user).order_by("created_at")

    records = Record.objects.filter(user_id=request.user).order_by("-updated_at")
    total_sums = (
        accounts.values("currency").annotate(sum=Sum("cur_amount")).order_by("-sum")
    )

    sum_items = []

    for sum in total_sums:
        currency = sum["currency"]
        currency_label = Account.Currency(currency).label
        sum_item = {**sum, "label": currency_label}
        sum_items.append(sum_item)

    if request.POST:
        if request.POST["_method"] == "account":
            form = AccountForm(request.POST)
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            Account.cal_cur_amount(account)
            return redirect("accounts:accounts")
        if request.POST["_method"] == "record":
            form = RecordForm(request.POST, user=request.user)
            if form.is_valid():
                record = form.save(commit=False)
                record.user = request.user
                record.save()
                return redirect("accounts:accounts")
        if request.POST["_method"] == "analyze":
            analysis = analyze_records(
                list(
                    records.filter(
                        updated_at__gt=datetime.now() - timedelta(days=30)
                    ).values("amount", "type", "category", "notes")
                ),
                days=30,
            )
            return render(
                request,
                "pages/accounts.html",
                {
                    "accounts": accounts,
                    "sums": sum_items,
                    "records": records,
                    "categories": categories,
                    "analysis": analysis,
                },
            )
    else:
        return render(
            request,
            "pages/accounts.html",
            {
                "accounts": accounts,
                "sums": sum_items,
                "records": records,
                "categories": categories,
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
