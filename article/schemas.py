from ninja import ModelSchema

from article.models import Article
from buckutt.types import PrimaryKey


class SimpleCategorySchema(ModelSchema):
    """
    Schéma de sérialisation pour une catégorie d'article
    ([Category][article.models.Category]).
    """

    class Config:
        model = Article
        model_fields = [
            "id",
            "name",
        ]


class SimpleArticleSchema(ModelSchema):
    """
    Schéma de sérialisation pour un article
    contenant uniquement son id, son nom et l'id de sa catégorie
    ([Article][article.models.Article]).
    """

    class Config:
        model = Article
        model_fields = [
            "id",
            "name",
            "category",
        ]


class AvailableArticleSchema(ModelSchema):
    """
    Schéma de sérialisation pour un article disponible,
    avec son id, son nom, l'id de sa catégorie, son stock, son prix
    et l'id de sa fondation
    ([Article][article.models.Article]).
    """

    class Config:
        model = Article
        model_fields = [
            "id",
            "name",
            "category",
            "stock",
        ]

    price: float
    foundation: PrimaryKey
