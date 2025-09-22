import graphene
from core.models import Order, Address
from core.graphql.public_identifier import CustomDjangoObjectType


class OrderType(CustomDjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"


class AddressType(CustomDjangoObjectType):
    class Meta:
        model = Address
        fields = "__all__"

    def resolve_phone_number(root, info):
        return (
            root.phone_number.as_international.replace(" ", "")
            if root.phone_number
            else ""
        )


class AddressInputType(graphene.InputObjectType):
    phone_number = graphene.String(required=True)
    street = graphene.String(required=True)
    city = graphene.String(required=True)
