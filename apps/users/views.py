from django.shortcuts import render, redirect
from .forms import UserForm


# Create your views here.
def register(request):
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sessions:new")
        else:
            return render(request, "pages/register.html", {"form": form})

    else:
        form = UserForm
        return render(request, "pages/register.html", {"form": form})
