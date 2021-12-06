from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.http.response import Http404
from django.shortcuts import redirect, render

from utils.helpers import forbidden_attributes

from core.forms import FormWithCaptcha
from core.models import Subscribers

from core.posts.models import Post
from core.accounts.forms import EditUserProfileForm, UserLoginForm, UserRegistrationForm
from core.accounts.models import User


def explore_users(request: HttpRequest):
    user_objects = User.objects.all().order_by("-datetime_joined")
    paginator = Paginator(user_objects, 20)

    try:
        page_number = int(request.GET.get("sida"))
    except:
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
    Logs user in on successful `User` instance creation
    """
    username = request.POST["username"]
    password = request.POST["password2"]

    user = authenticate(username=username.lower(), password=password)

    if user is not None:
        login(request, user)
        messages.success(
            request,
            "Welcome to Msukwini. You're among the first to join. So take a look around and tell me what you think.",
        )
        return redirect("posts:frontpage")
    else:
        messages.error(request, "Something went wrong")


def user_registration(request: HttpRequest):
    if request.user.is_authenticated:
        messages.error(
            request, "You can't create a new account while you're signed in."
        )
        return redirect("posts:frontpage")
    else:
        captcha = FormWithCaptcha

        if request.method == "POST":
            registration_form = UserRegistrationForm(request.POST)

            if registration_form.is_valid():
                registration_form.save()

                return login_user_on_register(request)
        else:
            registration_form = UserRegistrationForm()

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
    logout(request)
    return redirect("accounts:user-login")


def upgrade_user_account(request: HttpRequest):
    if request.method == "POST":
        subscribers, o = Subscribers.objects.get_or_create()
        subscribers.count += 1
        subscribers.save()
        messages.error(
            request,
            "Something went wrong. Your card details were not saved or processed. Please try again later.",
        )
        return redirect("accounts:upgrade")
    return render(request, "private/upgrade/credit_card_form.html")


def at_get_user_profile(request: HttpRequest, username: str):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404

    try:
        page_number = int(request.GET.get("sida"))
    except:
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
    forbidden_list = forbidden_attributes()
    for i in forbidden_list:
        if i.lower() in text.lower():
            return True
    return False


@login_required
def edit_user_profile(request: HttpRequest) -> HttpRequest:
    if request.method == "POST":
        edit_profile_form = EditUserProfileForm(
            request.POST, request.FILES, instance=request.user
        )

        if edit_profile_form.is_valid():
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
                    Continued use of these elements will result in a permanent ban from Msukwini. \
                    Please read our rules for more information about which tags and attributes are allowed.",
                )
        else:
            messages.error(request, "Bad request. Profile was not updated.")
    else:
        edit_profile_form = EditUserProfileForm(instance=request.user)
    context = {"user": request.user, "edit_profile_form": edit_profile_form}
    return render(request, "private/edit_profile.html", context)


@login_required
def delete_account(request: HttpRequest):
    if request.user.is_superuser:
        messages.error(
            request, "Admins need to use the admin site to delete their accounts"
        )
        return redirect("accounts:edit-user-profile")
    else:
        messages.success(request, "You account has been deleted")
        request.user.is_active = False
        request.user.save()
        return user_logout(request)
