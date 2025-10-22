from django.urls import path
from . import views

app_name = "records"

urlpatterns = [
    path("accounts/records/new", views.new_record, name="new_record"),
]
