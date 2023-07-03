from decimal import Decimal

from ninja import ModelSchema, Schema
from pydantic import Field

from buckutt.types import PrimaryKey
from transaction.models import Purchase


class PurchaseRequest(Schema):
    buyer_id: PrimaryKey
    selling_point_id: PrimaryKey
    articles: list[PrimaryKey]


class ReloadRequest(Schema):
    buyer_id: PrimaryKey
    selling_point_id: PrimaryKey
    amount: Decimal = Field(ge=0.01, decimal_places=2)


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
