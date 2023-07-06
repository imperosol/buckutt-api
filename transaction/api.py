from django.db import transaction
from django.db.models import Count, F, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja.params import Query
from ninja_extra.controllers import ControllerBase, api_controller, route

from article.models import Article
from selling_points.models import SellingPoint
from transaction.exceptions import NotEnoughCredit
from transaction.models import Cart, Purchase, Reload
from transaction.schemas import (
    PurchaseFilterSchema,
    PurchaseRequest,
    PurchaseSchema,
    PurchaseSummarySchema,
    ReloadFilterSchema,
    ReloadRequest,
    ReloadSchema,
    ReloadSummarySchema,
    TotalAmountSchema,
)
from users.models import User
from users.schemas import SimpleUserSchema


@api_controller("/purchase")
class PurchaseController(ControllerBase):
    """
    Contrôleur pour les achats.
    """
    @route.post("")
    @transaction.atomic
    def create(self, body: PurchaseRequest):
        """
        Crée une transaction.

        Args:
            body: Les informations de la transaction.
        """
        customer = get_object_or_404(User, pk=body.buyer_id)
        point = get_object_or_404(SellingPoint, pk=body.selling_point_id)
        seller = self.context.request.user
        cart = Cart(customer, seller, point)
        article_ids = sorted(body.articles)
        try:
            cart.add_articles(article_ids)
        except Article.DoesNotExist as e:
            raise Http404 from e
        if cart.total_price > customer.credit:
            raise NotEnoughCredit
        cart.save()

    @route.get("", response=list[PurchaseSchema])
    def fetch(self, filters: PurchaseFilterSchema = Query(...)):
        """
        Récupère les achats correspondant aux filtres donnés.

        Args:
            filters: Les filtres à appliquer.
        """
        return filters.filter(Purchase.objects.all())

    @route.get("/summary", response=list[PurchaseSummarySchema])
    def fetch_summary(self, filters: PurchaseFilterSchema = Query(...)):
        """
        Récupère un résumé des achats correspondant aux filtres donnés.

        Le résultat est sérialisé sous la forme d'une liste de
        [PurchaseSummarySchema][transaction.schemas.PurchaseSummarySchema].

        Args:
            filters: Les filtres à appliquer.
        """
        purchases = filters.filter(Purchase.objects.all())
        return (
            purchases.annotate(
                article_name=F("article__name"), point_name=F("point__name")
            )
            .values("article_name", "point_name", "price")
            .annotate(count=Count("pk"), total=Sum("price"))
        )


@api_controller("/reload")
class ReloadController(ControllerBase):
    """
    Contrôleur pour les rechargements.

    Les rechargements sont des transactions qui permettent à un utilisateur
    d'ajouter du crédit à son compte.
    """
    @route.post("", response=SimpleUserSchema)
    @transaction.atomic
    def create(self, body: ReloadRequest):
        """
        Crée un rechargement.

        Retourne l'utilisateur ayant effectué le rechargement
        sérialisé sous la forme d'un [SimpleUserSchema][users.schemas.SimpleUserSchema].

        Args:
            body: Les informations du rechargement.
        """
        customer = get_object_or_404(User, pk=body.buyer_id)
        Reload.objects.create(
            buyer=customer,
            point=get_object_or_404(SellingPoint, pk=body.selling_point_id),
            seller=self.context.request.user,
            amount=body.amount,
            trace="such",
        )
        customer.credit += body.amount
        customer.save()
        return customer

    @route.get("", response=list[ReloadSchema])
    def fetch(self, filters: ReloadFilterSchema = Query(...)):
        """
        Récupère les rechargements correspondant aux filtres donnés.

        Retourne une liste de [ReloadSchema][transaction.schemas.ReloadSchema].

        Args:
            filters: Les filtres à appliquer.
        """
        return filters.filter(Reload.objects.all())

    @route.get("/summary", response=list[ReloadSummarySchema])
    def fetch_summary(self, filters: ReloadFilterSchema = Query(...)):
        """
        Récupère un résumé des rechargements correspondant aux filtres donnés.

        Le résultat est sérialisé sous la forme d'une liste de
        [ReloadSummarySchema][transaction.schemas.ReloadSummarySchema].

        Args:
            filters: Les filtres à appliquer.
        """
        reloads = filters.filter(Reload.objects.all())
        return (
            reloads.annotate(point_name=F("point__name"))
            .values("point_name")
            .annotate(count=Count("pk"), total=Sum("amount"))
        )


@api_controller("/treasury")
class TreasuryController(ControllerBase):
    """
    Contrôleur pour la trésorerie.
    """
    @route.get("/global-credit", response=TotalAmountSchema)
    def get_total_credit(self):
        """
        Récupère le montant total du crédit de tous les utilisateurs.

        Le résultat est sérialisé sous la forme d'un
        [TotalAmountSchema][transaction.schemas.TotalAmountSchema].
        """
        return User.objects.all().aggregate(total=Sum("credit"))
