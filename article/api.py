from django.shortcuts import get_object_or_404
from ninja_extra.controllers import ControllerBase, api_controller, route

from article.models import Article
from article.schemas import AvailableArticleSchema
from selling_points.models import SellingPoint
from users.models import User


@api_controller("/article")
class ArticleController(ControllerBase):
    @route.get("/available-articles", response=list[AvailableArticleSchema])
    def fetch_available(self, selling_point_id: int, user_id: int):
        """
        Retourne tous les produits disponibles pour un utilisateur
        dans un point de vente, à l'instant présent, en annotant le prix
        de chaque produit pour l'utilisateur.

        Le prix du produit pour un utilisateur sera toujours le plus petit
        parmi les prix de tous les groupes auxquels l'utilisateur appartient.

        :param selling_point_id: id du point de vente
        :param user_id: id de l'utilisateur
        """
        selling_point = get_object_or_404(SellingPoint, pk=selling_point_id)
        customer = get_object_or_404(User, pk=user_id)
        return (
            Article.objects.available_now()
            .for_user(customer)
            .in_point(selling_point)
            .annotate_price_for(customer)
            .distinct()
        )
