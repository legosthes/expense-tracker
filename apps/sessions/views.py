from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect("accounts:accounts")
    return redirect("sessions:new")


@require_POST
def create(request):
    form = AuthenticationForm(request, data=request.POST)

    username = request.POST.get("username")
    password = request.POST.get("password")

    if not User.objects.filter(username=username).exists():
        form.add_error("username", f"The username: {username} is not registered.")

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
