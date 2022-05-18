from django.contrib import admin

from vetkoek.core.communities.models import Community


class CommunityAdmin(admin.ModelAdmin):
    search_fields = ("object_id",)


admin.site.register(Community, CommunityAdmin)
