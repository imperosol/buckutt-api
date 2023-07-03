from ninja import ModelSchema

from article.models import Article


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
