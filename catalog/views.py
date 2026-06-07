from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from catalog.models import Title
from catalog.services import CatalogService
from integrations.tmdb import TMDbClientError
from lists.forms import PersonalTitleStateForm
from lists.models import UserTitleState


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
        },
    )
