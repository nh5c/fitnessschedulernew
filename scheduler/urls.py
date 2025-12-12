# scheduler/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.session_list, name="session_list"),
    path("sessions/new/", views.session_create, name="session_create"),
    path("sessions/<int:pk>/edit/", views.session_update, name="session_update"),
    path("sessions/<int:pk>/delete/", views.session_delete, name="session_delete"),
    path("report/", views.session_report, name="session_report"),
]
