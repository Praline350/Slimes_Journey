from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Les compte user sont les comptes de viewers
    pass
