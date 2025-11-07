from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.records.forms import RecordForm
from apps.accounts.models import Account
from .models import Record
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_POST


@login_required
def account_record(request, account_id):
    categories = Record.ExpenseCategory
    records = Record.objects.filter(user=request.user, account=account_id).order_by(
        "-created_at"
    )
    return render(
        request,
        "pages/records.html",
        {"records": records, "selected": account_id, "categories": categories},
    )


@login_required
def category_record(request, category):
    categories = Record.ExpenseCategory
    records = Record.objects.filter(user=request.user, category=category).order_by(
        "-created_at"
    )
    return render(
        request, "pages/records.html", {"records": records, "categories": categories}
    )


@login_required
def account_category_record(request, account_id, category):
    categories = Record.ExpenseCategory
    records = Record.objects.filter(
        user=request.user, account=account_id, category=category
    ).order_by("-created_at")
    return render(
        request,
        "pages/records.html",
        {
            "records": records,
            "categories": categories,
            "selected": account_id,
        },
    )


@login_required
def sum_record(request, currency):
    categories = Record.ExpenseCategory
    currency_value = getattr(Account.Currency, currency)
    print(currency_value)
    accounts = Account.objects.filter(currency=currency_value)
    records = Record.objects.filter(user=request.user, account__in=accounts).order_by(
        "-created_at"
    )

    return render(
        request,
        "pages/records.html",
        {"records": records, "categories": categories},
    )


@login_required
def new_record(request):
    form = RecordForm(user=request.user)
    return render(request, "pages/new_record.html", {"form": form})


@login_required
def edit_record(request, record_id):
    record = Record.objects.get(pk=record_id)
    form = RecordForm(instance=record, user=request.user)
    return render(request, "pages/edit_record.html", {"form": form, "record": record})


@login_required
@require_POST
def update_record(request, record_id):
    record = Record.objects.get(pk=record_id)
    form = RecordForm(request.POST, instance=record, user=request.user)
    form.save()
    return redirect("accounts:accounts")


@login_required
@require_POST
def delete_record(request, record_id):
    record = Record.objects.get(pk=record_id, user=request.user)
    record.delete()
    response = HttpResponse(status=200)
    response["HX-Redirect"] = reverse("accounts:accounts")
    return response
