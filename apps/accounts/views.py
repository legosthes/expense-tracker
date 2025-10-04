from django.shortcuts import render


# Create your views here.
def accounts(request):
    return render(request, "pages/accounts.html")
