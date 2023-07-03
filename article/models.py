from django.contrib.auth.models import Group
from django.db import models
from django.db.models import OuterRef, Subquery
from django.utils.timezone import now

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class ArticleQuerySet(models.QuerySet):
    def available(self) -> "ArticleQuerySet":
        # noinspection PyTypeChecker
        return self.filter(is_removed=False)

    def available_now(self) -> "ArticleQuerySet":
        t = now()
        # noinspection PyTypeChecker
        return self.available().filter(
            prices__period__start__lte=t, prices__period__end__gte=t
        )

    def for_user(self, user: User) -> "ArticleQuerySet":
        # noinspection PyTypeChecker
        return self.filter(prices__group__in=user.groups.all())

    def in_point(self, point) -> "ArticleQuerySet":
        """
        :type point: selling_points.models.SellingPoint
        :param point:
        :return:
        """
        # noinspection PyTypeChecker
        return self.filter(selling_points=point)

    def annotate_price_for(self, user: User) -> "ArticleQuerySet":
        prices = Price.objects.filter(
            article=OuterRef("pk"), group__in=user.groups.all()
        )
        min_price = prices.order_by("amount").values("amount")[:1]
        # noinspection PyTypeChecker
        return self.annotate(price=Subquery(min_price))

    def annotate_foundation_for(self, user: User) -> "ArticleQuerySet":
        prices = Price.objects.filter(
            article=OuterRef("pk"), group__in=user.groups.all()
        )
        min_foundation = prices.order_by("amount").values("foundation_id")[:1]
        # noinspection PyTypeChecker
        return self.annotate(foundation=Subquery(min_foundation))


class Article(models.Model):
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
    name = models.CharField(max_length=40, unique=True)
    website = models.URLField()
    mail = models.EmailField(unique=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Period(models.Model):
    name = models.CharField(max_length=50, unique=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Price(models.Model):
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
