from django import forms

from core.posts.models import Post


class CreatePostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=140,
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
    caption = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "w-full text-black px-3 py-2 mb-3 border-2 border-gray-300 rounded bg-white",
                "placeholder": "Write your caption...",
                "autocomplete": "off",
                "autocapitalize": "off",
            }
        ),
    )
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "id": "selected-image",
                "required": "false",
            }
        ),
    )

    class Meta:
        model = Post
        fields = (
            "title",
            "caption",
            "image",
        )
