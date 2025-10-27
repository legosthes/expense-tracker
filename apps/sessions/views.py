from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
@require_POST
def create(request):
    form = AuthenticationForm(request, data=request.POST)

    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("accounts:accounts")
    else:
        return render(request, "pages/login.html", {"form": form})


def new(request):
    form = AuthenticationForm()
    return render(request, "pages/login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("sessions:new")
