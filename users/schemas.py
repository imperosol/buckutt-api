from ninja import ModelSchema

from users.models import User


class SimpleUserSchema(ModelSchema):
    """
    Schéma de données avec les informations de base d'un utilisateur.
    ([User][users.models.User]).
    """

    class Config:
        model = User
        model_fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        ]

    credit: float
