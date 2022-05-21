from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import include, path
from django.views.generic.base import TemplateView

from vetkoek.core.accounts.views import at_get_user_profile
from vetkoek.core.views import (
    about,
    index,
    news,
    privacy,
    rules,
    subscribe,
    terms,
)

handler404 = "vetkoek.core.views.handle_404"

urlpatterns = (
    [
        path("__debug__/", include("debug_toolbar.urls")),
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
        path("u/", include("vetkoek.core.accounts.urls", namespace="accounts")),
        # Post urls
        path("f/", include("vetkoek.core.posts.urls", namespace="posts")),
        # Search urls
        path("search/", include("vetkoek.core.search.urls", namespace="search")),
        # Communities urls
        path("b/", include("vetkoek.core.communities.urls", namespace="communities")),
        # Upgrade account
        path("join/", subscribe, name="subscribe"),
        path("@<username>/", at_get_user_profile, name="at-get-user"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

admin.site.site_header = "ViSpace Site Admin"
admin.site.site_title = "ViSpace Site Admin"

admin.site.unregister(Group)
