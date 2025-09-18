import graphene
import traceback
from core.graphql.product.types import (
    ProductType,
    CategoryInputType,
    ProductInputType,
)
from core.graphql.product.feedback import ProductFeedback
from siecom.decorators import logged_in_user_required


class CreateProduct(graphene.Mutation):
    class Arguments:
        products = graphene.List(ProductInputType, required=True)
        categories = graphene.List(CategoryInputType, required=True)

    success = graphene.Boolean()
    message = graphene.String()
    created_products = graphene.List(ProductType)

    @logged_in_user_required
    def mutate(root, info, products, categories):
        try:
            pass
        except Exception:
            traceback.print_exc()
            return CreateProduct(
                success=False,
                message=ProductFeedback.CREATION_ERROR,
                created_products=[],
            )
