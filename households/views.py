from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def household_dashboard(request):
    return render(request, "households/dashboard.html")
