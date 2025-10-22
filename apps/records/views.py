from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.records.forms import RecordForm


@login_required
def new_record(request):
    form = RecordForm(user=request.user)
    return render(request, "pages/new_record.html", {"form": form})
