from django.core.paginator import Paginator
from django.http.request import HttpRequest

from django.http.response import HttpResponse
from django.shortcuts import render

from core.communities.models import Community



def get_communities(request: HttpRequest) -> HttpResponse:
    qs = Community.objects.all().order_by("-datetime_created")

    paginator = Paginator(qs, 20)

    try:
        page_number = int(request.GET.get("sida"))
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    context = {
        "posts": qs,
        # "page_obj": page_obj,
    }
    return render(request, "public/communities.html", context)
