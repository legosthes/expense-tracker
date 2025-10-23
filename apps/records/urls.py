from django.urls import path
from . import views

app_name = "records"

urlpatterns = [
    path(
        "accounts/records/<int:account_id>", views.account_record, name="account_record"
    ),
    path("accounts/records/new", views.new_record, name="new_record"),
    path(
        "accounts/records/<int:record_id>/edit", views.edit_record, name="edit_record"
    ),
    path(
        "accounts/records/<int:record_id>/update",
        views.update_record,
        name="update_record",
    ),
    path(
        "accounts/records/<int:record_id>/delete",
        views.delete_record,
        name="delete_record",
    ),
]
