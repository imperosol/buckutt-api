from django.contrib.auth.models import Group
from django.db import models
from django.db.models import OuterRef, Subquery
from django.utils.timezone import now

from users.models import User


class Category(models.Model):
    """
    Représente une catégorie d'articles.

    Attributes:
        name (CharField): nom de la catégorie
    """

    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class ArticleQuerySet(models.QuerySet):
    """
    QuerySet personnalisé pour les articles.
    """

    def available(self) -> "ArticleQuerySet":
        """
        Filtre le queryset pour ne garder que les articles disponibles.

        Un article est considéré comme disponible si
        sa colonne `is_removed` est à False.
        """
        # noinspection PyTypeChecker
        return self.filter(is_removed=False)

    def available_now(self) -> "ArticleQuerySet":
        """
        Filtre le queryset pour ne garder que les articles disponibles
        à l'heure actuelle.

        Un article est considéré comme disponible maintenant si
        sa colonne is_removed est à False et qu'il possède au moins un prix
        applicable à l'heure actuelle.
        """
        t = now()
        # noinspection PyTypeChecker
        return self.available().filter(
            prices__period__start__lte=t, prices__period__end__gte=t
        )

    def for_user(self, user: User) -> "ArticleQuerySet":
        """
        Filtre le queryset pour ne garder que les articles
        possédant au moins un prix applicable à l'utilisateur donné.

        Args:
            user: l'utilisateur pour lequel les articles doivent être filtrés
        """
        # noinspection PyTypeChecker
        return self.filter(prices__group__in=user.groups.all())

    def in_point(self, point) -> "ArticleQuerySet":
        """
        Filtre le queryset pour ne garder que les articles
        vendus dans le point de vente donné.

        Args:
            point (selling_points.models.SellingPoint):
                le point de vente pour lequel les articles doivent être filtrés
        """
        # noinspection PyTypeChecker
        return self.filter(selling_points=point)

    def annotate_price_for(self, user: User) -> "ArticleQuerySet":
        """
        Annote le queryset avec le prix s'appliquant à l'utilisateur donné.

        Le prix d'un article pour un utilisateur est le prix le plus bas
        parmi ceux applicables à ce dernier.

        Args:
            user: l'utilisateur pour lequel le prix doit être annoté
        """
        prices = Price.objects.filter(
            article=OuterRef("pk"), group__in=user.groups.all()
        )
        min_price = prices.order_by("amount").values("amount")[:1]
        # noinspection PyTypeChecker
        return self.annotate(price=Subquery(min_price))

    def annotate_foundation_for(self, user: User) -> "ArticleQuerySet":
        """
        Annote le queryset avec la fondation s'appliquant à l'utilisateur donné.

        La fondation d'un article pour un utilisateur est la fondation
        associée au prix le plus bas parmi ceux applicables à l'utilisateur.

        Args:
            user: l'utilisateur pour lequel la fondation doit être annotée

        """
        prices = Price.objects.filter(
            article=OuterRef("pk"), group__in=user.groups.all()
        )
        min_foundation = prices.order_by("amount").values("foundation_id")[:1]
        # noinspection PyTypeChecker
        return self.annotate(foundation=Subquery(min_foundation))


class Article(models.Model):
    """
    Représente un article.

    Attributes:
        name (CharField): nom de l'article
        category (ForeignKey): catégorie de l'article
        stock (IntegerField): stock de l'article
        is_removed (BooleanField): indique si l'article est supprimé
    """

    name = models.CharField(max_length=40, unique=True)
    category = models.ForeignKey(
        to=Category, related_name="articles", on_delete=models.CASCADE
    )
    stock = models.IntegerField(default=-1)
    is_removed = models.BooleanField(default=False)

    objects = ArticleQuerySet.as_manager()

    def __str__(self):
        return self.name


class Foundation(models.Model):
    """
    Représente une fondation.

    Une fondation est une personne morale qui peut vendre des articles.
    Par exemple, le BDE est une fondation

    Attributes:
        name (CharField): nom de la fondation
        website (URLField): site web de la fondation
        mail (EmailField): adresse mail de la fondation
        is_removed (BooleanField): indique si la fondation est supprimée
    """

    name = models.CharField(max_length=40, unique=True)
    website = models.URLField()
    mail = models.EmailField(unique=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Period(models.Model):
    """
    Représente une période de validité d'un prix.

    Attributes:
        name (CharField): nom de la période
        start (DateTimeField): date de début de la période
        end (DateTimeField): date de fin de la période (optionnelle)
    """

    name = models.CharField(max_length=50, unique=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Price(models.Model):
    """
    Représente un prix d'un article pour une fondation et une période données.

    Unicité du prix:
        Il ne peut exister qu'un seul prix par ensemble article-fondation-période-group.

    Attributes:
        amount (DecimalField): montant du prix
        article (ForeignKey): article auquel le prix s'applique
        foundation (ForeignKey): fondation à laquelle le prix s'applique
        period (ForeignKey): période de validité du prix
        group (ForeignKey): groupe d'utilisateurs auquel le prix s'applique
        is_removed (BooleanField): indique si le prix est supprimé
    """

    amount = models.DecimalField(max_digits=8, decimal_places=2)
    article = models.ForeignKey(
        to=Article, related_name="prices", on_delete=models.CASCADE
    )
    foundation = models.ForeignKey(
        to=Foundation, related_name="prices", on_delete=models.CASCADE
    )
    period = models.ForeignKey(
        to=Period, related_name="prices", on_delete=models.CASCADE
    )
    group = models.ForeignKey(to=Group, related_name="prices", on_delete=models.CASCADE)

    is_removed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["article", "foundation", "period", "group"],
                name="unique_price",
            )
        ]

    def __str__(self):
        return f"{self.article.name} ({self.amount}€)"
