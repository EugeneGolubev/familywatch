from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def search(request):
    query = request.GET.get("q", "")
    return render(request, "catalog/search.html", {"query": query, "results": []})


@login_required
def title_detail(request, pk: int):
    return render(request, "catalog/title_detail.html", {"title_id": pk})
