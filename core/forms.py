from captcha.fields import ReCaptchaField
from django import forms
from django.contrib.auth.forms import UserChangeForm

from core.accounts.models import User


class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField(label="", required=True)


class EmailForm(UserChangeForm):
    email = forms.EmailField(
        required=True,
        max_length=200,
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

    class Meta:
        model = User
        fields = ("email",)
