from django.urls import path
from . import views

urlpatterns = [
    path("mine/", views.my_list, name="my_list"),
    path("household/", views.household_list, name="household_list"),
]
