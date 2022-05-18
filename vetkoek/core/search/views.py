import django
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http.request import HttpRequest
from django.shortcuts import render

from vetkoek.core.accounts.models import User
from vetkoek.core.posts.models import Post


@login_required
def advanced_search(request: HttpRequest):
    """
    We're looping through all the models we want to search, then looping through all the fields in those models, then
    creating a query for each field, then combining all those queries into one, then searching the model with that query,
    then adding the results to a list, then adding all the lists to another list, then passing that list to the template

    :param request: The request object
    :type request: HttpRequest
    :return: A list of objects that match the search query.
    """
    search_query = request.GET.get("q")

    if not search_query:
        return render(request, "public/search/search.html")
    else:
        search_models = [User, Post]
        search_results = []
        final_results = []

        for model in search_models:
            fields = [
                x
                for x in model._meta.fields
                if isinstance(x, django.db.models.CharField)
            ]
            search_queries = [
                Q(**{x.name + "__contains": search_query}) for x in fields
            ]
            q_object = Q()

            for query in search_queries:
                q_object = q_object | query

            results = model.objects.filter(q_object)
            search_results.append(results)

            for i in search_results:
                final_results.append(i)

        context = {"query": search_query, "results": final_results}
        return render(request, "public/search/results.html", context)


def search(request: HttpRequest):
    """
    If the user has entered a search query, then we search for users that match the query and display the results. If the
    user hasn't entered a search query, then we display the search page

    :param request: The request object
    :type request: HttpRequest
    :return: A search query is being returned.
    """
    search_query = request.GET.get("q")

    if search_query:
        qs = (
            User.objects.filter(
                Q(username__icontains=search_query)
                | Q(display_name__icontains=search_query)
            ).order_by("-last_login").exclude(is_active=False)[:20]
        )

        paginator = Paginator(qs, 20)

        try:
            page_number = int(request.GET.get("sida"))
        except ValueError:
            page_number = 1

        page_obj = paginator.get_page(page_number)

        context = {"query": search_query, "page": "search", "page_obj": page_obj}
        return render(request, "public/search/results.html", context)
    else:
        if request.user.is_authenticated:
            qs = (
                User.objects.all()
                    .order_by("-datetime_joined")
                    .exclude(object_id=request.user.object_id)[:7]
            )
        else:
            qs = User.objects.all().order_by("-datetime_joined")[:7]
        paginator = Paginator(qs, 15)

        try:
            page_number = int(request.GET.get("sida"))
        except ValueError:
            page_number = 1

        page_obj = paginator.get_page(page_number)

        context = {"page": "search", "page_obj": page_obj}
        return render(request, "public/search/search.html", context)
