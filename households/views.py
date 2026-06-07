from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import HouseholdCreateForm
from .services import (
    HouseholdService,
    get_household_for_member,
    get_membership,
    households_for_user,
    user_is_household_owner,
)


@login_required
def household_dashboard(request):
    households = households_for_user(request.user)
    return render(request, "households/dashboard.html", {"households": households})


@login_required
def household_create(request):
    if request.method == "POST":
        form = HouseholdCreateForm(request.POST)
        if form.is_valid():
            household = HouseholdService.create_household_for_user(
                user=request.user,
                name=form.cleaned_data["name"],
                default_country=form.cleaned_data["default_country"],
            )
            return redirect("household_detail", pk=household.pk)
    else:
        form = HouseholdCreateForm()
    return render(request, "households/create.html", {"form": form})


@login_required
def household_detail(request, pk: int):
    household = get_household_for_member(user=request.user, pk=pk)
    membership = get_membership(user=request.user, household=household)
    return render(
        request,
        "households/detail.html",
        {
            "household": household,
            "membership": membership,
            "is_owner": user_is_household_owner(request.user, household),
        },
    )
