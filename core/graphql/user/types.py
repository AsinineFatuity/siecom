from core.graphql.public_identifier import CustomDjangoObjectType
from core.models import User


class UserType(CustomDjangoObjectType):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number"]
