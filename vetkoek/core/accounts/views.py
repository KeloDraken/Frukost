from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from core.forms import FormWithCaptcha
from core.accounts.forms import UserLoginForm, UserRegistrationForm
from core.accounts.models import User


def explore_users(request: HttpRequest) -> HttpResponse:
    user_objects = User.objects.all().order_by("-datetime_joined")
    paginator = Paginator(user_objects, 20)

    try:
        page_number = int(request.GET.get("sida"))
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    context = {"heading": "Cool new people", "page_obj": page_obj}
    return render(request, "public/frontpage/explore_users.html", context)


def request_has_valid_captcha(request: HttpRequest) -> bool:
    """
    Checks if request object has valid captcha
    """
    captcha_data = request.POST["g-recaptcha-response"]
    if not captcha_data == "" and captcha_data is not None:
        return True
    return False


def login_user_on_register(request: HttpRequest) -> HttpResponseRedirect:
    """
    Logs user in on successful `User` instance creation
    """
    username = request.POST["email"]
    password = request.POST["password2"]

    user = authenticate(username=username.lower(), password=password)

    if user is not None:
        login(request, user)
        messages.success(request, "Welcome to  Feel free to explore.")
        return redirect("posts:frontpage")
    else:
        messages.error(request, "Something went wrong")


def user_registration(request: HttpRequest) -> HttpResponse:
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
def user_logout(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    return redirect("accounts:user-login")


def change_web_url(user: User, website: str) -> None:
    if not len(website) <= 0 and not website == None:
        user.website = website
    else:
        user.website = None


def change_twitter_handle(user: User, twitter: str) -> None:
    if not len(twitter) <= 0 and not twitter == None:
        user.twitter = twitter
    else:
        user.twitter = None


def change_instagram_handle(user: User, instagram: str) -> None:
    if not len(instagram) <= 0 and not instagram == None:
        user.instagram = instagram
    else:
        user.instagram = None


def change_display_name(user: User, display_name: str) -> None:
    if not len(display_name) <= 0 and not display_name == None:
        user.display_name = display_name
    else:
        pass


def change_bio(request: HttpRequest, user: User, bio: str) -> None:
    if len(bio) > 220:
        messages.error(
            request, "Your bio is too long. Please keep it at 220 characters of less"
        )
    else:
        user.bio = bio


def update_profile_pic(request: HttpRequest, user: User) -> None:
    if request.FILES.get("profile_pic"):
        user.profile_pic = request.FILES.get("profile_pic")


def save_profile(request: HttpRequest) -> None:
    """
    Continues to save other fields in Edit Profile
    """
    user = request.user

    update_profile_pic(request, user)

    bio = request.POST["about_me"]

    change_bio(request, user, bio)

    display_name = request.POST["display_name"]
    change_display_name(user, display_name)

    instagram = request.POST["instagram"]
    change_instagram_handle(user, instagram)

    twitter = request.POST["twitter"]
    change_twitter_handle(user, twitter)

    website = request.POST["website"]
    change_web_url(user, website)

    user.save()
    messages.success(request, "Profile successfully updated")


def get_user_profile(request: HttpRequest, username: str):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "public/404.html")

    context = {"user": user}
    return render(request, "public/user_profile.html", context)


@login_required
def edit_user_profile(request: HttpRequest) -> HttpRequest:
    if request.method == "POST":
        return save_profile(request)

    context = {
        "user": request.user,
    }
    return render(request, "private/accounts/edit_profile.html", context)


@login_required
def delete_account(request: HttpRequest) -> HttpResponseRedirect:
    if request.user.is_superuser:
        messages.error(
            request, "Admins need to use the admin site to delete their accounts"
        )
        return redirect("accounts:user-dashboard")
    else:
        messages.success(request, "You account has been deleted")
        request.user.is_active = False
        request.user.save()
        return user_logout(request)
