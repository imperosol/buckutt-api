from decimal import Decimal

from django.contrib.postgres.aggregates import ArrayAgg
from django.db import IntegrityError, models
from django.db.models import OuterRef

from article.models import Article, Foundation, Price
from buckutt.types import PrimaryKey
from selling_points.models import SellingPoint
from users.models import User


class Purchase(models.Model):
    """
    Représente un achat d'article.

    Attributes:
        date (DateTimeField): date et heure de l'achat
        price (DecimalField): prix de l'achat
        buyer (ForeignKey[User]): acheteur
        seller (ForeignKey[User]): vendeur
        article (ForeignKey[Article]): article acheté
        point (ForeignKey[SellingPoint]): point de vente ou l'achat a été effectué
        foundation (ForeignKey[Foundation]): fondation à laquelle l'achat est associé

    Redondance du prix:
        La colonne `price` peut sembler redondante, sachant qu'il y a la colonne `article`,
        à partir de laquelle on peut remonter au prix de l'article.
        Cependant, il est possible que ledit prix vienne à être modifié, et il est important
        de garder une trace du prix au moment de l'achat.
    """

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

    Il s'agit d'une classe intermédiaire pour faciliter
    la création d'un groupe d'achats à partir d'une liste
    de clefs primaires d'articles.

    Il ne s'agit pas d'un modèle de données.
    La classe `Cart` ne correspond pas à une table de la base de données.

    Examples:
        ```python
        from transaction.models import Cart
        from users.models import User
        from selling_points.models import SellingPoint
        customer = User.objects.get(pk=1)
        seller = User.objects.get(pk=2)
        point = SellingPoint.objects.get(pk=1)
        cart = Cart(customer, seller, point)
        ```

        Une fois le panier créé, l'ajout d'articles se fait en appelant la méthode
        [add_article][transaction.models.Cart.add_articles]
        avec une liste d'ids d'articles :

        ```python
        cart.add_articles([1, 2, 3])
        cart.add_articles([4, 5, 6])
        cart.save()  # enregistre les achats correspondant aux articles dans la db
        ```
    """

    def __init__(self, customer: User, seller: User, point: SellingPoint):
        """
        Args:
            customer: L'utilisateur qui achète les articles
            seller: L'utilisateur qui vend les articles
            point: Le point de vente où l'achat est effectué
        """
        self.customer = customer
        self.seller = seller
        self.point = point
        self.purchases: list[Purchase] = []

    def add_articles(self, ids: list[PrimaryKey]):
        """
        Ajoute les articles dont les ids sont donnés
        à la liste des articles du panier.

        Args:
            ids: liste des ids des articles à ajouter au panier

        Raises:
            Article.DoesNotExist: si un des ids donnés ne correspond à
                aucun article disponible à la vente pour l'utilisateur.

        Warning:
            L'appel de cette méthode effectue une requête à la base de données
            pour récupérer les articles correspondants aux ids donnés.
            Essayez de ne l'utiliser qu'une seule fois par panier.
        """
        if len(ids) == 0:
            return
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

    def save(self) -> None:
        """
        Enregistre les achats dans la base de données et retire le montant
        correspondant du compte de l'utilisateur.

        Raises:
            IntegrityError: si le solde du compte de l'utilisateur est insuffisant
        """
        total = self.total_price
        if total > self.customer.credit:
            raise IntegrityError(
                "Le solde du compte est insuffisant"
                f" ({self.customer.credit}€) pour effectuer l'achat ({total}€)"
            )
        Purchase.objects.bulk_create(self.purchases)
        self.customer.credit -= total
        self.customer.save()
        self.purchases = []

    @property
    def total_price(self) -> Decimal:
        """
        Prix total des articles dans le panier.
        """
        return sum(a.price for a in self.purchases)


class Reload(models.Model):
    """
    Représente un rechargement du compte d'un utilisateur.

    Un rechargement est effectué par un utilisateur
    et est effectué par un vendeur dans un point de vente.

    Le montant du rechargement est ajouté au solde du compte de l'utilisateur.

    Attributes:
        date (DateTimeField): Date et heure du rechargement
        amount (DecimalField): Montant du rechargement
        trace (CharField): Trace du rechargement (pour les paiements par carte)
        buyer (ForeignKey[User]): Utilisateur dont le compte est rechargé
        seller (ForeignKey[User]): Utilisateur qui effectue le rechargement
        point (ForeignKey[SellingPoint]): Point de vente où le rechargement est effectué
    """

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
