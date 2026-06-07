from django.urls import path
from . import views

urlpatterns = [
    path("mine/", views.my_list, name="my_list"),
    path("mine/titles/<int:title_pk>/", views.personal_title_state, name="personal_title_state"),
    path("mine/titles/<int:title_pk>/remove/", views.remove_personal_title_state, name="remove_personal_title_state"),
    path("households/<int:household_pk>/", views.household_lists, name="household_lists"),
    path("households/<int:household_pk>/create/", views.create_household_list, name="create_household_list"),
    path("households/<int:household_pk>/<int:list_pk>/", views.household_list_detail, name="household_list_detail"),
    path("households/<int:household_pk>/<int:list_pk>/add/", views.add_household_list_title, name="add_household_list_title"),
    path(
        "households/<int:household_pk>/<int:list_pk>/items/<int:item_pk>/remove/",
        views.remove_household_list_item,
        name="remove_household_list_item",
    ),
    path("household/", views.household_list, name="household_list"),
]
