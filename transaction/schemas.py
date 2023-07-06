from datetime import datetime
from decimal import Decimal

from ninja import FilterSchema, ModelSchema, Schema
from pydantic import Field, PositiveInt

from buckutt.types import PrimaryKey
from transaction.models import Purchase


class PurchaseRequest(Schema):
    """
    Valide les données nécessaires pour créer un achat.

    Attributes:
        buyer_id (PrimaryKey): id de l'acheteur
        selling_point_id (PrimaryKey): id du point de vente
        articles (list[PrimaryKey]): liste des ids des articles
    """

    buyer_id: PrimaryKey
    selling_point_id: PrimaryKey
    articles: list[PrimaryKey]


class ReloadRequest(Schema):
    """
    Valide les données nécessaires pour créer un rechargement.

    Attributes:
        buyer_id (PrimaryKey): id de l'acheteur
        selling_point_id (PrimaryKey): id du point de vente
        amount (Decimal): montant du rechargement
    """

    buyer_id: PrimaryKey
    selling_point_id: PrimaryKey
    amount: Decimal = Field(ge=0.01, decimal_places=2)


class PurchaseSchema(ModelSchema):
    """
    Schéma de sérialisation pour un achat
    ([Purchase][transaction.models.Purchase]).
    """

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
    """
    Schéma de sérialisation pour un rechargement
    ([Reload][transaction.models.Reload]).
    """

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
    """
    Schéma de filtrage pour les recherches d'achats.

    Attributes:
        before_date (datetime): pour les achats avant cette date
        after_date (datetime): pour les achats après cette date
        buyer_id (PrimaryKey): pour sélectionner les achats d'un acheteur
        foundation_id (PrimaryKey): pour sélectionner les achats d'une fondation
    """

    before_date: datetime | None = Field(q="date__lte")
    after_date: datetime | None = Field(q="date__gte")
    buyer_id: PrimaryKey | None
    foundation_id: PrimaryKey | None


class PurchaseSummarySchema(Schema):
    """
    Schéma de sérialisation pour un résumé d'achat.

    Attributes:
        article_name (str): nom de l'article
        point_name (str): nom du point de vente
        price (float): prix de l'article
        count (PositiveInt): nombre d'articles achetés
        total (float): prix total de l'achat
    """

    article_name: str
    point_name: str
    price: float
    count: PositiveInt
    total: float


class ReloadFilterSchema(FilterSchema):
    """
    Schéma de filtrage pour les recherches de rechargements.

    Attributes:
        before_date (datetime): pour les rechargements avant cette date
        after_date (datetime): pour les rechargements après cette date
        buyer_id (PrimaryKey): pour sélectionner les rechargements d'un acheteur
    """

    before_date: datetime | None = Field(q="date__lte")
    after_date: datetime | None = Field(q="date__gte")
    buyer_id: PrimaryKey | None


class ReloadSummarySchema(Schema):
    """
    Schéma de sérialisation pour un résumé de rechargement.

    Attributes:
        point_name (str): nom du point de vente
        count (PositiveInt): nombre de rechargements
        total (float): montant total des rechargements
    """

    point_name: str
    count: PositiveInt
    total: float


class TotalAmountSchema(Schema):
    """
    Schéma de sérialisation pour un montant total.

    Attributes:
        total (float): montant total
    """

    total: float
