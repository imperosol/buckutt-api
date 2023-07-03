from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pin = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    credit = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    is_temporary = models.BooleanField(default=False)
    failed_auth = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.username
