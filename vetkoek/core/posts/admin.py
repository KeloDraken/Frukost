from django.contrib import admin

from vetkoek.core.posts.models import Post, Tag


class PostAdmin(admin.ModelAdmin):
    search_fields = ("object_id",)


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
