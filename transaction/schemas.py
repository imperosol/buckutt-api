from ninja import ModelSchema, Schema

from buckutt.types import PrimaryKey
from transaction.models import Purchase


class PurchaseRequest(Schema):
    buyer_id: PrimaryKey
    selling_point_id: PrimaryKey
    articles: list[PrimaryKey]


class PurchaseResponse(ModelSchema):
    class Config:
        model = Purchase
        model_fields = [
            "id",
            "price",
            "article",
            "seller",
            "point",
            "date",
            "foundation",
        ]
        depth = 2
