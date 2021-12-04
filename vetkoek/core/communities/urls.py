from django.urls import path
from core.communities.views import get_communities


app_name = "communities"

urlpatterns = [
    path("", get_communities, name="get-communities"),
]