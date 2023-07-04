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
    ReloadRequest, ReloadSchema, ReloadFilterSchema, ReloadSummarySchema, TotalAmountSchema,
)
from users.models import User
from users.schemas import SimpleUserSchema


@api_controller("/purchase")
class PurchaseController(ControllerBase):
    @route.post("")
    @transaction.atomic
    def create(self, body: PurchaseRequest):
        """
        Crée une transaction.
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
        return filters.filter(Purchase.objects.all())

    @route.get("/summary", response=list[PurchaseSummarySchema])
    def fetch_summary(self, filters: PurchaseFilterSchema = Query(...)):
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
    @route.post("", response=SimpleUserSchema)
    @transaction.atomic
    def create(self, body: ReloadRequest):
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
        return filters.filter(Reload.objects.all())

    @route.get("/summary", response=list[ReloadSummarySchema])
    def fetch_summary(self, filters: ReloadFilterSchema = Query(...)):
        reloads = filters.filter(Reload.objects.all())
        return (
            reloads.annotate(point_name=F("point__name"))
            .values("point_name")
            .annotate(count=Count("pk"), total=Sum("amount"))
        )


@api_controller("/treasury")
class TreasuryController(ControllerBase):
    @route.get("/global-credit", response=TotalAmountSchema)
    def get_total_credit(self):
        return User.objects.all().aggregate(total=Sum("credit"))
