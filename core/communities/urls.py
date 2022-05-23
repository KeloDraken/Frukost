from django.urls import path

from core.communities.views import get_communities, get_community

app_name = "communities"

urlpatterns = [
    path("", get_communities, name="get-communities"),
    path("<name>/", get_community, name="get-community"),
]
