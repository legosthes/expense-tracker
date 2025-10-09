from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [path("accounts/<int:id>", views.accounts, name="accounts")]
