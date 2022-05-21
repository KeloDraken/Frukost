from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from vetkoek.core.accounts.models import User
from vetkoek.utils.helpers import object_id_generator


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "w-full text-black px-3 py-2 mb-3 border-2 border-gray-300 rounded bg-white",
                "placeholder": "Required",
                "autocomplete": "off",
                "autocapitalize": "off",
            }
        ),
    )
    password1 = forms.CharField(
        max_length=60,
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full text-black px-3 py-2 mb-3 border-2 border-gray-300 rounded bg-white",
                "placeholder": "Required",
                "id": "password",
                "autocomplete": "false",
                "autocapitalize": "off",
            }
        ),
    )
    password2 = forms.CharField(
        max_length=60,
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full text-black px-3 py-2 mb-3 border-2 border-gray-300 rounded bg-white",
                "placeholder": "Required",
                "id": "password",
                "autocomplete": "none",
                "autocapitalize": "off",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        username = self.cleaned_data["username"]
        user.display_name = username
        user.object_id = object_id_generator(11, User)
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=30,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "w-full text-black px-3 py-2 mb-3 border-2 border-gray-300 rounded bg-white",
                "placeholder": "Required",
                "autocomplete": "off",
                "name": "Username",
                "autocapitalize": "off",
                "autofocus": "true",
            }
        ),
    )
    password = forms.CharField(
        max_length=60,
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full text-black px-3 py-2 mb-3 border-2 border-gray-300 rounded bg-white",
                "placeholder": "Required",
                "id": "password",
                "name": "Password",
                "autocomplete": "false",
                "autocapitalize": "off",
            }
        ),
    )
    error_messages = {
        "invalid_login": _("Incorrect log in credentials"),
        "inactive": _("This account has been suspended"),
    }

    def confirm_login_allowed(self, user: User):
        if not user.is_active:
            raise ValidationError(
                "This account is inactive.",
                code="inactive",
            )


class EditUserProfileForm(UserChangeForm):
    profile_pic = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "id": "selected-image",
            }
        ),
    )

    display_name = forms.CharField(
        max_length=100,
        required=True,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "w-full text-black px-3 py-2 mb-3 border-2 border-gray-300 rounded bg-white",
                "placeholder": "Required",
                "autocomplete": "off",
                "name": "display_name",
                "autocapitalize": "off",
            }
        ),
    )

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "w-full text-black px-3 py-2 mb-3 border-2 border-gray-300 rounded bg-white",
                "placeholder": "Tell us about yourself...",
                "autocomplete": "off",
                "autocapitalize": "off",
            }
        ),
    )
    # custom_html = forms.CharField(
    #     required=False,
    #     widget=forms.Textarea(
    #         attrs={
    #             "class": "w-full text-black px-3 py-2 mb-3 border-2 border-gray-300 rounded bg-white",
    #             "placeholder": "Paste your custom styles here...",
    #             "autocomplete": "off",
    #             "autocapitalize": "off",
    #         }
    #     ),
    # )

    class Meta:
        model = User
        fields = (
            "profile_pic",
            "display_name",
            "bio",
            # "custom_html",
        )
