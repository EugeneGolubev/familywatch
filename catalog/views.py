from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect

from catalog.models import Title
from catalog.services import CatalogService
from integrations.tmdb import TMDbClientError
from lists.forms import HouseholdCategoryChoiceForm, PersonalTitleStateForm
from lists.models import UserTitleState
from lists.services import HouseholdListService, get_title_or_404


@login_required
def search(request):
    query = request.GET.get("q", "")
    response = CatalogService().search(query)
    return render(
        request,
        "catalog/search.html",
        {
            "query": response.query,
            "results": response.results,
            "error_message": response.error_message,
        },
    )


@login_required
def title_detail(request, pk: int):
    media_type = request.GET.get("type")
    title = None
    error_message = ""

    if media_type:
        try:
            title = CatalogService().get_or_sync_title(media_type=media_type, tmdb_id=pk)
        except TMDbClientError as exc:
            error_message = str(exc)
    else:
        title = get_object_or_404(Title, pk=pk)

    personal_state = UserTitleState.objects.filter(user=request.user, title=title).first() if title else None

    return render(
        request,
        "catalog/title_detail.html",
        {
            "title": title,
            "error_message": error_message,
            "personal_state": personal_state,
            "personal_form": PersonalTitleStateForm(instance=personal_state) if title else None,
            "household_category_form": HouseholdCategoryChoiceForm(user=request.user) if title else None,
        },
    )


@login_required
def add_title_to_household_category(request, title_pk: int):
    if request.method != "POST":
        return redirect("title_detail", pk=title_pk)

    title = get_title_or_404(pk=title_pk)
    form = HouseholdCategoryChoiceForm(request.POST, user=request.user)
    if form.is_valid():
        household_list = form.cleaned_data["household_list"]
        _, created = HouseholdListService.add_title(
            user=request.user,
            household_pk=household_list.household_id,
            list_pk=household_list.pk,
            title=title,
        )
        if created:
            messages.success(request, "Title added to the household category.")
        else:
            messages.info(request, "That title is already in this household category.")
    else:
        messages.error(request, "Choose one of your household categories.")
    return redirect("title_detail", pk=title.pk)
