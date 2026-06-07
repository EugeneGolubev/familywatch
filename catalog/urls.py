from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.search, name="catalog_search"),
    path("titles/<int:pk>/", views.title_detail, name="title_detail"),
]
