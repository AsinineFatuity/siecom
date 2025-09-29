import graphene
import traceback
from django.db.models import Avg
from core.models import Product, Category
from core.graphql.product.feedback import ProductFeedback
from core.graphql.product.types import AverageCategoryPriceType, ProductType


class ProductQuery(graphene.ObjectType):
    average_price_per_category = graphene.Field(
        AverageCategoryPriceType, category_id=graphene.ID(required=True)
    )
    products = graphene.List(ProductType, category_id=graphene.ID(required=False))

    def resolve_average_price_per_category(root, info, category_id):
        try:
            category = Category.objects.get_object_by_public_id(category_id)
            if not category:
                return AverageCategoryPriceType(
                    success=False,
                    message=ProductFeedback.CATEGORY_DOES_NOT_EXIST,
                    average_price=0.0,
                    category=None,
                )
            category: Category = category
            categories = category.descendants(include_self=True)
            average_price = (
                Product.objects.filter(category__in=categories).aggregate(
                    avg_price=Avg("price")
                )["avg_price"]
                or 0.0
            )
            return AverageCategoryPriceType(
                success=True,
                message=ProductFeedback.AVERAGE_PRICE_CALCULATION_SUCCESS,
                average_price=round(average_price, 2),
                category=category,
            )

        except Exception:
            traceback.print_exc()
            return AverageCategoryPriceType(
                success=False,
                message=ProductFeedback.AVERAGE_PRICE_CALCULATION_ERROR,
                average_price=0.0,
                category=None,
            )

    def resolve_products(root, info, category_id):
        try:
            products = Product.objects.select_related("category").all()
            if category_id:
                products = products.filter(category__public_id=category_id)
            return products
        except Exception:
            traceback.print_exc()
            return []
