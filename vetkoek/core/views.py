from datetime import datetime
import random

from django.contrib import messages
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from utils.helpers import object_id_generator

from core.forms import EmailForm
from core.models import Feedback, News, Privacy, Rules, Terms


def handle_404(request: HttpRequest) -> HttpResponse:
    return render(request, "public/404.html")


def generate_random_num_once_a_day():
    d0 = datetime(2008, 8, 18) 
    d1 = datetime.now()
    delta = d1 - d0
    random.seed(delta.days)
    return random.randint(3,13)

def subscribe(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to upgrade your account")
        return redirect("accounts:user-login")
    else:
        if request.method == "POST":
            if request.POST.get("email"):
                email = request.POST.get("email")
                request.user.email = email
                request.user.save()
                return redirect("accounts:upgrade")
            else:
                messages.error(request, "Something went wrong. Please try again.")
                return redirect("accounts:email")
        else:
            form = EmailForm()
        num_joined = generate_random_num_once_a_day()
        context = {"form": form, "num_joined": num_joined}
        return render(request, "private/upgrade/email_form.html", context)


def add_feedback(request: HttpRequest) -> HttpResponseRedirect:
    if request.method == "POST":
        feedback = request.POST.get("feedback")

        if not len(feedback) <= 0 and not feedback == None:
            object_id = object_id_generator(11, Feedback)
            Feedback.objects.create(object_id=object_id, body=feedback)

            messages.success(
                request, "Thank you for the feedback. We will review it soon"
            )
            return redirect("about")

        else:
            messages.error(
                request, "Something went wrong. We couldn't send your feedback"
            )
            return redirect("about")


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "public/index.html")


def news(request: HttpRequest) -> HttpResponse:
    news_ = News.objects.all().order_by("-datetime_created")
    context = {"heading": "Foxstraat News", "news": news_}
    return render(request, "views/blog/news.html", context)


def about(request: HttpRequest) -> HttpResponse:
    add_feedback(request)
    return render(request, "views/index.html", context={"page": "about"})


def terms(request: HttpRequest) -> HttpResponse:
    news_ = Terms.objects.all()
    context = {"heading": "Terms of Service", "news": news_}
    return render(request, "views/blog/news.html", context)


def privacy(request: HttpRequest) -> HttpResponse:
    news_ = Privacy.objects.all()
    context = {"heading": "Privacy Policy", "news": news_}
    return render(request, "views/blog/news.html", context)


def rules(request: HttpRequest) -> HttpResponse:
    news_ = Rules.objects.all()
    context = {"heading": "Foxstraat Rules", "news": news_}
    return render(request, "views/blog/news.html", context)
