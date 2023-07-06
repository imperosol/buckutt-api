from ninja import ModelSchema

from selling_points.models import SellingPoint


class SimplePointSchema(ModelSchema):
    """
    Schéma de sérialisation pour un point de vente
    contenant uniquement son id et son nom
    ([SellingPoint][selling_points.models.SellingPoint]).
    """
    class Config:
        model = SellingPoint
        model_fields = [
            "id",
            "name",
        ]
