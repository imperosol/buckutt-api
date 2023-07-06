from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Utilisateur du système. Remplace la classe auth.User de Django

    Cette classe comprend tous les attributs de la classe
    django.contrib.auth.models.AbstractUser et y ajoute les attributs suivants :

    Attributes:
        pin (CharField): code PIN de l'utilisateur
        nickname (Charfield): surnom de l'utilisateur
        credit (DecimalField): crédit de l'utilisateur (0 par défaut)
        is_temporary (BooleanField): si l'utilisateur est temporaire (False par défaut)
        failed_auth (BooleanField): si l'utilisateur a échoué à s'authentifier (False par défaut)
        is_removed (BooleanField): si l'utilisateur est supprimé (False par défaut)
    """

    pin = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    credit = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    is_temporary = models.BooleanField(default=False)
    failed_auth = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.username
