from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja_extra.controllers import ControllerBase, api_controller, route

from article.models import Article
from selling_points.models import SellingPoint
from transaction.exceptions import NotEnoughCredit
from transaction.models import Cart
from transaction.schemas import PurchaseRequest
from users.models import User


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
