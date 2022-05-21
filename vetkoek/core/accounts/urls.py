from django.urls import path

from vetkoek.core.accounts.views import (
    delete_account,
    explore_users,
    user_registration,
    user_login,
    user_logout,
    edit_user_profile,
    upgrade_user_account,
    user_themes,
)

app_name = "accounts"

urlpatterns = [
    path("register/", user_registration, name="user-register"),
    path("login/", user_login, name="user-login"),
    path("logout/", user_logout, name="user-logout"),
    path("edit/", edit_user_profile, name="edit-user-profile"),
    path("explore/", explore_users, name="explore-users"),
    path("upgrade/", upgrade_user_account, name="upgrade"),
    path("delete/", delete_account, name="delete-user"),
    path("themes/", user_themes, name="user-themes"),
]
