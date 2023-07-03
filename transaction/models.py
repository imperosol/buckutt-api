from django.db import models

from article.models import Article, Foundation
from selling_points.models import SellingPoint
from users.models import User


class Purchase(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    buyer = models.ForeignKey(
        to=User, related_name="purchases", on_delete=models.PROTECT
    )
    seller = models.ForeignKey(to=User, related_name="sales", on_delete=models.PROTECT)
    article = models.ForeignKey(
        to=Article, related_name="purchases", on_delete=models.PROTECT
    )
    point = models.ForeignKey(
        to=SellingPoint, related_name="purchases", on_delete=models.PROTECT
    )
    foundation = models.ForeignKey(
        to=Foundation, related_name="purchases", on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.buyer} - {self.article} ({self.price}€)"


class Reload(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    trace = models.CharField(max_length=50)

    buyer = models.ForeignKey(to=User, related_name="reloads", on_delete=models.PROTECT)
    seller = models.ForeignKey(
        to=User, related_name="reloads_as_seller", on_delete=models.PROTECT
    )
    point = models.ForeignKey(
        to=SellingPoint, related_name="reloads", on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.buyer} - {self.date} ({self.amount}€)"
