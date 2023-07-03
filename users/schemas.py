from ninja import ModelSchema

from users.models import User


class SimpleUserSchema(ModelSchema):
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
