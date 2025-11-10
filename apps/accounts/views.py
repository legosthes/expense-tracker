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


# Create your views here.
@login_required
def accounts(request):
    categories = Record.ExpenseCategory
    accounts = (
        Account.objects.filter(user_id=request.user)
        .annotate(
            # calculating the total_expenses within the query
            total_expenses=Sum(
                Case(
                    When(records__type="Expense", then="records__amount"),
                    # non-matching will become 0
                    default=0,
                    output_field=DecimalField(max_digits=20, decimal_places=2),
                )
            ),
            # calculating the total_incomes within the query
            total_incomes=Sum(
                Case(
                    (When(records__type="Income", then="records__amount")),
                    default=0,
                    output_field=DecimalField(max_digits=20, decimal_places=2),
                )
            ),
        )
        .order_by("created_at")
    )

    # calculating the cur_amount without using the function in the model because it'll query too many times
    for account in accounts:
        account.cur_amount = (
            account.init_amount
            # if value is None, use 0
            + (account.total_incomes or 0)
            - (account.total_expenses or 0)
        )

    # update all the accounts at once
    Account.objects.bulk_update(accounts, ["cur_amount"])

    records = Record.objects.filter(user_id=request.user).order_by("-created_at")
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
