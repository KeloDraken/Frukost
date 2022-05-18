from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.shortcuts import redirect, render

from vetkoek.core.communities.models import Community


def get_communities(request: HttpRequest):
    """
    It gets all the communities from the database, orders them by the date they were created, and then paginates them

    :param request: The request object
    :type request: HttpRequest
    :return: A list of all the communities.
    """
    qs = Community.objects.all().order_by("-datetime_created")

    paginator = Paginator(qs, 20)

    try:
        page_number = int(request.GET.get("sida"))
    except ValueError:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    context = {
        "posts": qs,
        "page_obj": page_obj,
    }
    return render(request, "public/communities.html", context)


def get_community(request: HttpRequest, name: str):
    """
    It gets a community by name, or redirects to the subscribe page if it doesn't exist

    :param request: The request object that was sent to the view
    :type request: HttpRequest
    :param name: The name of the community
    :type name: str
    :return: A redirect to the subscribe page.
    """
    try:
        community = Community.objects.get(title=name)
    except Community.DoesNotExist:
        pass
    return redirect("subscribe")
