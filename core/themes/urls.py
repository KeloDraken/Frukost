from django.urls import path
from core.themes.views import get_themes


app_name = "themes"

urlpatterns = [
    path("", get_themes, name="get-themes"),
]
