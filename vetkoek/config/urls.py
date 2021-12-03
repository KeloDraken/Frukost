from django.contrib import admin
from django.contrib.auth.models import Group

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import TemplateView
from django.urls import include, path, re_path

from core.views import (
    about,
    handle_404,
    index,
    news,
    privacy,
    rules,
    terms,
)
from core.accounts.views import get_user_profile


urlpatterns = (
    [
        path("", index, name="index"),
        path("u/admin/", admin.site.urls, name="admin"),
        path("about/", about, name="about"),
        path("news/", news, name="news"),
        path(
            "robots.txt",
            TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        ),
        # Legal
        path("privacy/", privacy, name="privacy"),
        path("rules/", rules, name="rules"),
        path("terms/", terms, name="terms"),
        # Accounts urls
        path("u/", include("core.accounts.urls", namespace="accounts")),
        path("<username>/", get_user_profile, name="get-user-profile"),

        # 404
        # re_path((r"^(\d+)/(\d+)$", handle_404),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

admin.site.site_header = "Foxstraat Site Admin"
admin.site.site_title = "Foxstraat Site Admin"

admin.site.unregister(Group)
