from django.db import models

from article.models import Article


class SellingPoint(models.Model):
    name = models.CharField(max_length=50)
    articles = models.ManyToManyField(to=Article, related_name="selling_points")
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=50)
    selling_point = models.ForeignKey(
        to=SellingPoint, related_name="devices", on_delete=models.CASCADE
    )
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
