from django.urls import path

from core.posts.views import create_post, get_post, frontpage, delete_post


app_name = "posts"

urlpatterns = [
    path("", frontpage, name="frontpage"),
    path("add/", create_post, name="create-post"),
    path("delete/<post_id>", delete_post, name="delete-post"),
    path("<post_id>/", get_post, name="get-post"),
]
