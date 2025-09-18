import graphene
from core.graphql.public_identifier import CustomDjangoObjectType
from core.models import Product, Category


class ProductType(CustomDjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class CategoryType(CustomDjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryInputType(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)


class ProductInputType(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int(required=True)
