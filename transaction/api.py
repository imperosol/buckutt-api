from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from ninja_extra.controllers import ControllerBase, api_controller, route

from article.models import Article
from selling_points.models import SellingPoint
from transaction.models import Purchase
from transaction.schemas import PurchaseRequest
from users.models import User


@api_controller("/purchase")
class PurchaseController(ControllerBase):
    @route.post("")
    def create(self, body: PurchaseRequest):
        """
        Crée une transaction.
        """
        customer = get_object_or_404(User, pk=body.buyer_id)
        seller = self.context.request.user
        point = get_object_or_404(SellingPoint, pk=body.selling_point_id)
        article_ids = sorted(body.articles)
        articles = list(Article.objects.available_now().filter(pk__in=article_ids))
        if len(articles) != len(article_ids):
            # Si certains articles n'ont pas été trouvés par la requête db,
            # ça signifie que la requête HTTP a transmis des id inexistants
            bad_ids = set(article_ids) - {a.id for a in articles}
            raise Http404(f"Can't resolve those articles : {bad_ids}")
        cart: list[Purchase] = []
        t = now()
        for article_id in body.articles:
            cart.append(
                Purchase(
                    date=t,
                    point=point,
                    seller=seller,
                    buyer=customer,
                    article_id=article_id,
                    price=Article.objects.get(pk=1),
                )
            )
