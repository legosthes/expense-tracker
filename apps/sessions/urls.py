from django.urls import path
from . import views

app_name = "sessions"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.new, name="new"),
    path("create/", views.create, name="create"),
    path("logout/", views.logout_user, name="logout"),
]
