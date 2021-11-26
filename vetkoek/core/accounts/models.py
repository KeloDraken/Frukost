from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Users within the ChafPozi authentication system are represented by this model.

    Username and password are required. Other fields are optional.
    """
    pass

