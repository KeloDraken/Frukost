from django.contrib import admin

from core.accounts.models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ("username",)
    list_display = (
        "object_id",
        "username",
        "date_joined",
    )


admin.site.register(User, UserAdmin)
