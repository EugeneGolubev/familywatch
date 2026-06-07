from django.urls import path
from . import views

urlpatterns = [
    path("", views.household_dashboard, name="household_dashboard"),
    path("create/", views.household_create, name="household_create"),
    path("<int:pk>/", views.household_detail, name="household_detail"),
]
