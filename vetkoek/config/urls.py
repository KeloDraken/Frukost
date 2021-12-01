from django.contrib import admin
from django.contrib.auth.models import Group

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import TemplateView
from django.urls import include, path

from core.views import (
    about,
    index,
    news,
    privacy,
    rules,
    terms,
)

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
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

admin.site.site_header = "Foxstraat Site Admin"
admin.site.site_title = "Foxstraat Site Admin"

admin.site.unregister(Group)
