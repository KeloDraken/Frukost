from django.urls import path

from core.accounts.views import (
    delete_account,
    explore_users,
    get_user_profile,
    user_registration,
    user_login,
    user_logout,
    edit_user_profile,
    upgrade_user_account,
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
    path("<username>/", get_user_profile, name="get-user-profile"),
]
