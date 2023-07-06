from django.db import models

from article.models import Article


class SellingPoint(models.Model):
    """
    Représente un point de vente.

    Attributes:
        name (CharField): nom du point de vente
        articles (ManyToManyField[Article]): articles vendus dans ce point de vente
        is_removed (BooleanField): indique si le point de vente est supprimé
    """

    name = models.CharField(max_length=50)
    articles = models.ManyToManyField(to=Article, related_name="selling_points")
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Device(models.Model):
    """
    Représente un appareil utilisé pour la vente.

    Attributes:
        name (CharField): nom de l'appareil
        selling_point (ForeignKey[SellingPoint]): point de vente dans lequel l'appareil est utilisé
        is_removed (BooleanField): indique si l'appareil est supprimé
    """

    name = models.CharField(max_length=50)
    selling_point = models.ForeignKey(
        to=SellingPoint, related_name="devices", on_delete=models.CASCADE
    )
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
