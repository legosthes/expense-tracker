from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("accounts/", views.accounts, name="accounts"),
    path("accounts/new/", views.new_account, name="new_account"),
    path(
        "accounts/account/<int:account_id>/edit",
        views.edit_account,
        name="edit_account",
    ),
    path(
        "accounts/account/<int:account_id>/update",
        views.update_account,
        name="update_account",
    ),
    path(
        "accounts/account/<int:account_id>/delete",
        views.delete_account,
        name="delete_account",
    ),
]
