from django.contrib import admin

from core.accounts.models import User


class UserAdmin(admin.ModelAdmin):
    """
    User model admin manager
    """

    pass


admin.site.register(User, UserAdmin)
