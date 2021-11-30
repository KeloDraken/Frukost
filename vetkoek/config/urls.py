from django.contrib import admin
from django.contrib.auth.models import Group

from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]

admin.site.site_header = "ChafPozi Admin Site"
admin.site.site_title = "ChafPozi Admin Site"

admin.site.unregister(Group)
