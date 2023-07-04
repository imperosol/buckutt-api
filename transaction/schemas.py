from datetime import datetime
from decimal import Decimal

from ninja import FilterSchema, ModelSchema, Schema
from pydantic import Field, PositiveInt

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


class PurchaseSchema(ModelSchema):
    class Config:
        model = Purchase
        model_fields = [
            "id",
            "article",
            "buyer",
            "seller",
            "point",
            "date",
            "foundation",
        ]

    price: float


class ReloadSchema(ModelSchema):
    class Config:
        model = Purchase
        model_fields = [
            "id",
            "buyer",
            "seller",
            "point",
            "date",
        ]
    amount: float


class PurchaseFilterSchema(FilterSchema):
    before_date: datetime | None = Field(q="date__lte")
    after_date: datetime | None = Field(q="date__gte")
    buyer_id: PrimaryKey | None
    foundation_id: PrimaryKey | None


class PurchaseSummarySchema(Schema):
    article_name: str
    point_name: str
    price: float
    count: PositiveInt
    total: float


class ReloadFilterSchema(FilterSchema):
    before_date: datetime | None = Field(q="date__lte")
    after_date: datetime | None = Field(q="date__gte")
    buyer_id: PrimaryKey | None


class ReloadSummarySchema(Schema):
    point_name: str
    count: PositiveInt
    total: float


class TotalAmountSchema(Schema):
    total: float
