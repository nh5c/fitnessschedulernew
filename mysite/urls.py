# mysite/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # All main app URLs (fitness scheduler)
    path("", include("scheduler.urls")),
]
