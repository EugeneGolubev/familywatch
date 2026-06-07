from django.urls import path
from . import views

urlpatterns = [path("", views.household_dashboard, name="household_dashboard")]
