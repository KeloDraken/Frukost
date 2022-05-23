from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import include, path
from django.views.generic.base import TemplateView

from core.accounts.views import at_get_user_profile
from core.views import (
    about,
    index,
    news,
    privacy,
    rules,
    subscribe,
    terms,
)

handler404 = "core.views.handle_404"

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
        path("u/", include("core.accounts.urls", namespace="accounts")),
        # Post urls
        path("f/", include("core.posts.urls", namespace="posts")),
        # Search urls
        path("search/", include("core.search.urls", namespace="search")),
        # Communities urls
        path("b/", include("core.communities.urls", namespace="communities")),
        # Themes urls
        path("t/", include("core.themes.urls", namespace="themes")),
        # Upgrade account
        path("join/", subscribe, name="subscribe"),
        path("@<username>/", at_get_user_profile, name="at-get-user"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

admin.site.site_header = "Frukost Site Admin"
admin.site.site_title = "Frukost Site Admin"

admin.site.unregister(Group)
