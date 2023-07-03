from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models
from django.db.models import OuterRef

from article.models import Article, Foundation, Price
from buckutt.types import PrimaryKey
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


class Cart:
    """
    Représente un panier d'achat.

    Classe intermédiaire pour faciliter la création d'un groupe d'achats
    à partir d'une liste de clefs primaires d'articles.
    """

    def __init__(self, customer: User, seller: User, point: SellingPoint):
        self.customer = customer
        self.seller = seller
        self.point = point
        self.purchases: list[Purchase] = []

    def add_articles(self, ids: list[PrimaryKey]):
        """
        Ajoute les articles dont les ids sont donnés
        à la liste des articles du panier.

        Si certains des id données ne correspondent pas à des articles,
        lève une exception.
        """
        ids = sorted(ids)
        prices = Price.objects.filter(
            article=OuterRef("pk"), group__in=self.customer.groups.all()
        )
        articles = (
            Article.objects.available_now()
            .filter(pk__in=ids)
            .annotate(price=ArrayAgg(prices.values("amount")[:1]))
            .annotate_price_for(self.customer)
            .annotate_foundation_for(self.customer)
            .distinct()
        )
        if len(articles) != len(ids):
            bad_ids = set(ids) - {a.pk for a in articles}
            raise Article.DoesNotExist(
                f"Les articles suivants n'existent pas : {bad_ids}"
            )
        purchases = [
            Purchase(
                price=a.price,
                buyer=self.customer,
                seller=self.seller,
                article=a,
                point=self.point,
                foundation_id=a.foundation,
            )
            for a in articles
        ]
        self.purchases.extend(purchases)

    def save(self):
        """
        Enregistre les achats dans la base de données.
        """
        Purchase.objects.bulk_create(self.purchases)
        self.customer.credit -= self.total_price
        self.customer.save()
        self.purchases = []

    @property
    def total_price(self):
        return sum(a.price for a in self.purchases)


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
