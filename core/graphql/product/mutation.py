import graphene
import traceback
from siecom.decorators import logged_in_user_required
from core.graphql.product.types import (
    ProductType,
    CategoryInputType,
    ProductInputType,
)
from core.graphql.product.feedback import ProductFeedback
from core.models import Product, Category


class CreateProduct(graphene.Mutation):
    """
    NOTE: Assumes that uploaded products have same category
    such that the category is a list of the hierarchy with the last item being the most specific.
    """

    class Arguments:
        products = graphene.List(ProductInputType, required=True)
        categories = graphene.List(CategoryInputType, required=True)

    success = graphene.Boolean()
    message = graphene.String()
    created_products = graphene.List(ProductType)

    @logged_in_user_required
    def mutate(root, info, products, categories):
        try:
            product_names = [p.name.lower() for p in products]
            if len(product_names) != len(set(product_names)):
                return CreateProduct(
                    success=False,
                    message=ProductFeedback.DUPLICATE_PRODUCT_NAME,
                    created_products=[],
                )
            category_names = [c.name.lower() for c in categories]
            if len(category_names) != len(set(category_names)):
                return CreateProduct(
                    success=False,
                    message=ProductFeedback.DUPLICATE_CATEGORY_NAME,
                    created_products=[],
                )
            specific_category = Category.create_category_hierarchy(categories)
            created_products = Product.create_products(products, specific_category)
            return CreateProduct(
                success=True,
                message=ProductFeedback.PRODUCT_CREATION_SUCCESS,
                created_products=created_products,
            )

        except Exception:
            traceback.print_exc()
            return CreateProduct(
                success=False,
                message=ProductFeedback.CREATION_ERROR,
                created_products=[],
            )
