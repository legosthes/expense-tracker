from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.accounts.urls")),
    path("", include("apps.users.urls")),
    path("", include("apps.records.urls")),
    path("", include("apps.sessions.urls")),
]
