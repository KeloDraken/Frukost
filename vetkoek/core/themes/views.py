from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect


def get_themes(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("accounts:user-login")
    return render(request, "private/themes/themes.html")
