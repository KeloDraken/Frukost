from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render

from vetkoek.core.accounts.forms import (
    EditUserProfileForm,
    UserLoginForm,
    UserRegistrationForm,
)
from vetkoek.core.accounts.models import User
from vetkoek.core.forms import FormWithCaptcha
from vetkoek.core.models import Subscribers
from vetkoek.core.posts.models import Post
from vetkoek.utils.helpers import forbidden_attributes


def explore_users(request: HttpRequest):
    """
    "Get all users, order them by date joined, paginate them, and render them in a template."

    The first thing we do is get all users from the database. We order them by date joined, so that the newest users are at
    the top. We then create a paginator object, which is a Django object that handles pagination. We pass it the list of
    users, and tell it that we want 20 users per page

    :param request: The request object
    :type request: HttpRequest
    :return: A list of all users, ordered by the date they joined.
    """
    user_objects = User.objects.all().order_by("-datetime_joined")
    paginator = Paginator(user_objects, 20)

    try:
        page_number = int(request.GET.get("sida"))
    except ValueError:
        page_number = 1
    except TypeError:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    context = {"heading": "Cool new people", "page_obj": page_obj}
    return render(request, "public/explore_users.html", context)


def request_has_valid_captcha(request: HttpRequest) -> bool:
    """
    Checks if request object has valid captcha
    """
    captcha_data = request.POST["g-recaptcha-response"]
    if not captcha_data == "" and captcha_data is not None:
        return True
    return False


def login_user_on_register(request: HttpRequest):
    """
    It takes a request object, creates a user object, and logs the user in

    :param request: HttpRequest
    :type request: HttpRequest
    :return: A function that takes a request and returns a redirect to the frontpage.
    """
    username = request.POST["username"]
    password = request.POST["password2"]

    user = authenticate(username=username.lower(), password=password)

    if user is not None:
        login(request, user)
        messages.success(
            request,
            "Welcome to ViSpace. You're among the first to join. So take a look around and tell me what you think.",
        )
        return redirect("posts:frontpage")
    else:
        messages.error(request, "Something went wrong")


def user_registration(request: HttpRequest):
    """
    If the user is not authenticated, then show the registration form

    :param request: HttpRequest
    :type request: HttpRequest
    :return: A rendered template.
    """
    if request.user.is_authenticated:
        messages.error(
            request, "You can't create a new account while you're signed in."
        )
        return redirect("posts:frontpage")
    else:
        captcha = FormWithCaptcha()

        if not request.method == "POST":
            registration_form = UserRegistrationForm()

        else:
            registration_form = UserRegistrationForm(request.POST)

            if registration_form.is_valid():
                registration_form.save()
                return login_user_on_register(request)

        context = {
            "registration_form": registration_form,
            "captcha": captcha,
        }
        return render(request, "public/auth/registration_form.html", context)


class UserLoginView(LoginView):
    template_name = "public/auth/login_form.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True


user_login = UserLoginView.as_view()


@login_required
def user_logout(request: HttpRequest):
    """
    It logs out the user and redirects them to the login page

    :param request: The request object is passed to the view function by Django
    :type request: HttpRequest
    :return: The user is being redirected to the login page.
    """
    logout(request)
    return redirect("accounts:user-login")


def upgrade_user_account(request: HttpRequest):
    """
    "If the request method is not POST, render the credit card form. Otherwise, increment the subscriber count and redirect
    to the upgrade page."

    The problem is that the function is doing too much. It's responsible for rendering the credit card form, incrementing
    the subscriber count, and redirecting to the upgrade page

    :param request: The request object
    :type request: HttpRequest
    :return: A redirect to the upgrade page.
    """
    if not request.method == "POST":
        return render(request, "private/upgrade/credit_card_form.html")

    subscribers, o = Subscribers.objects.get_or_create()
    subscribers.count += 1
    subscribers.save()
    messages.error(
        request,
        "Something went wrong. Your card details were not saved or processed. Please try again later.",
    )
    return redirect("accounts:upgrade")


def at_get_user_profile(request: HttpRequest, username: str):
    """
    It gets a user's profile page

    :param request: The request object
    :type request: HttpRequest
    :param username: str
    :type username: str
    :return: A HttpResponse object with the rendered template.
    """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404

    try:
        page_number = int(request.GET.get("sida"))
    except ValueError:
        page_number = 1
    except TypeError:
        page_number = 1

    qs = Post.objects.filter(user=user).order_by("-datetime_created")
    paginator = Paginator(qs, 15)
    page_obj = paginator.get_page(page_number)

    context = {
        "user": user,
        "page_obj": page_obj,
    }
    return render(request, "public/user_profile.html", context)


def is_dirty_html(text: str):
    """
    It returns True if the text contains any of the forbidden attributes

    :param text: The text to be checked
    :type text: str
    :return: True or False
    """
    forbidden_list = forbidden_attributes()
    for i in forbidden_list:
        if i.lower() in text.lower():
            return True
    return False


@login_required
def edit_user_profile(request: HttpRequest) -> HttpRequest:
    """
    It takes a request, checks if it's a POST request, and if it is, it checks if the form is valid, and if it is, it saves
    the form

    :param request: The request object is a parameter that's passed to all views in Django. It contains metadata about the
    request, including the HTTP method
    :type request: HttpRequest
    :return: A HttpRequest object.
    """
    if not request.method == "POST":
        edit_profile_form = EditUserProfileForm(instance=request.user)
    else:
        edit_profile_form = EditUserProfileForm(
            request.POST, request.FILES, instance=request.user
        )

        if not edit_profile_form.is_valid():
            messages.error(request, "Bad request. Profile was not updated.")
        else:
            edit_profile_form.save(commit=False)

            if request.FILES.get("profile_pic") is None:
                edit_profile_form.profile_pic = request.user.profile_pic

            if not is_dirty_html(request.POST.get("custom_html")):
                messages.success(request, "Profile updated")
                edit_profile_form.save()
            else:
                messages.error(
                    request,
                    "Your template contains forbidden elements. \
                    Continued use of these elements will result in a permanent ban from ViSpace. \
                    Please read our rules for more information about which tags and attributes are allowed.",
                )
    context = {"user": request.user, "edit_profile_form": edit_profile_form}
    return render(request, "private/edit_profile.html", context)


@login_required
def delete_account(request: HttpRequest):
    """
    If the user is a superuser, they can't delete their account from the frontend, so we redirect them to the edit profile
    page with an error message. If they're not a superuser, we delete their account and redirect them to the login page with
    a success message

    :param request: The request object is a parameter that's passed to every view in Django. It contains metadata about the
    current web request that's being processed
    :type request: HttpRequest
    :return: The user is being returned.
    """
    if request.user.is_superuser:
        messages.error(
            request, "Admins need to use the admin site to delete their accounts"
        )
        return redirect("accounts:edit-user-profile")
    else:
        messages.success(request, "You account has been deleted")
        request.user.delete()
        return redirect("accounts:user-login")
