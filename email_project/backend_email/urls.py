from django.urls import path
from . import views

urlpatterns = [
    path("validate_emails/",views.ValidateEmailsView.as_view(), name="validate_emails"),
]