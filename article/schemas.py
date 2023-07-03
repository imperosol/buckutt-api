from ninja import ModelSchema

from article.models import Article
from buckutt.types import PrimaryKey


class AvailableArticleSchema(ModelSchema):
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
