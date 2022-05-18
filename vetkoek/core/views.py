import random
from datetime import datetime

from django.contrib import messages
from django.http.request import HttpRequest
from django.shortcuts import redirect, render

from vetkoek.core.forms import EmailForm
from vetkoek.core.models import Feedback, News, Privacy, Rules, Terms
from vetkoek.utils.helpers import object_id_generator


def handle_404(request: HttpRequest, exception):
    """
    "When a 404 error occurs, render the public/404.html template."

    :param request: The request that caused the 404 error
    :type request: HttpRequest
    :param exception: The exception raised by the view function
    :return: A response object.
    """
    return render(request, "public/404.html")


def generate_random_num_once_a_day():
    """
    It generates a random number between 3 and 13, but it only generates a new random number once a day
    :return: A random number between 3 and 24.
    """
    d0 = datetime(2008, 8, 18)
    d1 = datetime.now()
    delta = d1 - d0
    random.seed(delta.days)
    return random.randint(3, 24)


def subscribe(request):
    """
    If the user is logged in, and the request method is POST, and the POST request has an email, then save the email to the
    user's account, and redirect to the upgrade page

    :param request: The request object is a Python object that contains all the information about the request that was sent
    to the server
    :return: A render of the email_form.html page.
    """
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
                return redirect("subscribe")
        else:
            if request.user.email is not None and not request.user.email == "":
                return redirect("accounts:upgrade")

            form = EmailForm()
        num_joined = generate_random_num_once_a_day()
        context = {"form": form, "num_joined": num_joined}
        return render(request, "private/upgrade/email_form.html", context)


def add_feedback(request: HttpRequest):
    """
    It takes the feedback from the user and saves it in the database

    :param request: The request object
    :type request: HttpRequest
    :return: A function that takes a request and returns a redirect to the about page
    """
    if request.method == "POST":
        feedback = request.POST.get("feedback")

        if not len(feedback) <= 0 and feedback is not None:
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


def index(request: HttpRequest):
    """
    It takes an HTTP request and returns an HTML page

    :param request: This is the request object that Django uses to pass information from the browser to the server
    :type request: HttpRequest
    :return: The index.html file is being returned.
    """
    return render(request, "public/index.html")


def news(request: HttpRequest):
    """
    It gets all the news from the database, and then passes it to the news.html template

    :param request: The request object
    :type request: HttpRequest
    :return: A list of all the news objects in the database.
    """
    news_ = News.objects.all().order_by("-datetime_created")
    context = {"heading": "ViSpace News", "news": news_}
    return render(request, "views/blog/news.html", context)


def about(request: HttpRequest):
    """
    It renders the `views/index.html` template, passing in the `page` variable with the value `about`

    :param request: The request object
    :type request: HttpRequest
    :return: A render object.
    """
    add_feedback(request)
    return render(request, "views/index.html", context={"page": "about"})


def terms(request: HttpRequest):
    """
    It takes a request, gets all the terms of service from the database, and then renders the terms of service page

    :param request: This is the request object that is sent to the view
    :type request: HttpRequest
    :return: A list of all the terms of service.
    """
    news_ = Terms.objects.all()
    context = {"heading": "Terms of Service", "news": news_}
    return render(request, "views/blog/news.html", context)


def privacy(request: HttpRequest):
    """
    It takes an HTTP request, gets the first Privacy object from the database, and then renders the news.html template with
    the heading "Privacy Policy" and the news object

    :param request: This is the request object that is sent to the view
    :type request: HttpRequest
    :return: A function that takes a request and returns a response.
    """
    news_ = Privacy.objects.first()
    context = {"heading": "Privacy Policy", "news": news_}
    return render(request, "public/news.html", context)


def rules(request: HttpRequest):
    """
    It takes a request, gets the first object from the Rules model, and then renders the news.html template with the heading
    "ViSpace Rules" and the news object.

    :param request: This is the request object that is sent to the view
    :type request: HttpRequest
    :return: A HttpResponse object with the rendered template passed to the constructor.
    """
    news_ = Rules.objects.first()
    context = {"heading": "ViSpace Rules", "news": news_}
    return render(request, "public/news.html", context)
