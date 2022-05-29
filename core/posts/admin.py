from django.contrib import admin

from core.posts.models import Post, Tag


class PostAdmin(admin.ModelAdmin):
    search_fields = ("object_id", "title", "caption",)


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
