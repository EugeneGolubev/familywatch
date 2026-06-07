from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def my_list(request):
    return render(request, "lists/my_list.html")


@login_required
def household_list(request):
    return render(request, "lists/household_list.html")
