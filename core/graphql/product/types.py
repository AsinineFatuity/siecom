import graphene
from core.graphql.public_identifier import CustomDjangoObjectType
from core.models import Product, Category


class ProductType(CustomDjangoObjectType):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "category"]


class CategoryType(CustomDjangoObjectType):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class CategoryInputType(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    description = graphene.String(required=True)


class ProductInputType(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int(required=True)
