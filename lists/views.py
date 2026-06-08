from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from catalog.models import Title
from lists.forms import HouseholdListAddTitleForm, HouseholdListCreateForm, PersonalTitleStateForm
from lists.models import HouseholdList, UserTitleState
from lists.services import HouseholdListService, PersonalTitleStateService, get_title_or_404


@login_required
def my_list(request):
    selected_status = request.GET.get("status", "")
    states = PersonalTitleStateService.list_for_user(user=request.user, status=selected_status)
    return render(
        request,
        "lists/my_list.html",
        {
            "states": states,
            "selected_status": selected_status,
            "status_choices": UserTitleState.Status.choices,
        },
    )


@login_required
def personal_title_state(request, title_pk: int):
    title = get_title_or_404(pk=title_pk)
    instance = UserTitleState.objects.filter(user=request.user, title=title).first()

    if request.method != "POST":
        return redirect("title_detail", pk=title.pk)

    form = PersonalTitleStateForm(request.POST, instance=instance)
    if form.is_valid():
        PersonalTitleStateService.add_or_update(
            user=request.user,
            title=title,
            status=form.cleaned_data["status"],
            rating=form.cleaned_data["rating"],
            notes=form.cleaned_data["notes"],
            watched_at=form.cleaned_data["watched_at"],
        )
        messages.success(request, "Personal state saved.")
    else:
        messages.error(request, "Check your personal state details.")
    return redirect("title_detail", pk=title.pk)


@login_required
def remove_personal_title_state(request, title_pk: int):
    title = get_title_or_404(pk=title_pk)
    if request.method == "POST":
        PersonalTitleStateService.remove(user=request.user, title=title)
        messages.success(request, "Title removed from your list.")
    return redirect("my_list")


@login_required
def household_lists(request, household_pk: int):
    household, lists = HouseholdListService.lists_for_household(user=request.user, household_pk=household_pk)
    return render(
        request,
        "lists/household_overview.html",
        {
            "household": household,
            "household_lists": lists,
            "form": HouseholdListCreateForm(),
        },
    )


@login_required
def create_household_list(request, household_pk: int):
    if request.method != "POST":
        return redirect("household_lists", household_pk=household_pk)

    form = HouseholdListCreateForm(request.POST)
    if form.is_valid():
        household_list, created = HouseholdListService.create_list(
            user=request.user,
            household_pk=household_pk,
            name=form.cleaned_data["name"],
        )
        if created:
            messages.success(request, "Household list created.")
        else:
            messages.info(request, "That household list already exists.")
        return redirect("household_list_detail", household_pk=household_pk, list_pk=household_list.pk)

    household, lists = HouseholdListService.lists_for_household(user=request.user, household_pk=household_pk)
    return render(
        request,
        "lists/household_overview.html",
        {
            "household": household,
            "household_lists": lists,
            "form": form,
        },
        status=400,
    )


@login_required
def household_list_detail(request, household_pk: int, list_pk: int):
    try:
        household_list = HouseholdListService.get_list_for_member(
            user=request.user,
            household_pk=household_pk,
            list_pk=list_pk,
        )
    except HouseholdList.DoesNotExist as exc:
        raise Http404 from exc

    items = household_list.items.select_related("title", "added_by").order_by("-added_at", "-id")
    return render(
        request,
        "lists/household_detail.html",
        {
            "household": household_list.household,
            "household_list": household_list,
            "items": items,
            "add_form": HouseholdListAddTitleForm(),
        },
    )


@login_required
def add_household_list_title(request, household_pk: int, list_pk: int):
    if request.method != "POST":
        return redirect("household_list_detail", household_pk=household_pk, list_pk=list_pk)

    form = HouseholdListAddTitleForm(request.POST)
    if form.is_valid():
        title = Title.objects.get(pk=form.cleaned_data["title_pk"])
        try:
            _, created = HouseholdListService.add_title(
                user=request.user,
                household_pk=household_pk,
                list_pk=list_pk,
                title=title,
            )
        except HouseholdList.DoesNotExist as exc:
            raise Http404 from exc
        if created:
            messages.success(request, "Title added to the household list.")
        else:
            messages.info(request, "That title is already on this household list.")
    else:
        messages.error(request, "Choose an existing local title.")
    return redirect("household_list_detail", household_pk=household_pk, list_pk=list_pk)


@login_required
def remove_household_list_item(request, household_pk: int, list_pk: int, item_pk: int):
    if request.method == "POST":
        try:
            HouseholdListService.remove_item(
                user=request.user,
                household_pk=household_pk,
                list_pk=list_pk,
                item_pk=item_pk,
            )
        except HouseholdList.DoesNotExist as exc:
            raise Http404 from exc
        messages.success(request, "Title removed from the household list.")
    return redirect("household_list_detail", household_pk=household_pk, list_pk=list_pk)


@login_required
def household_list(request):
    return redirect("household_dashboard")
