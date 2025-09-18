import graphene
from django.db.models import Avg
from core.models import Product
from siecom.decorators.authorization import logged_in_user_required


class ProductQuery(graphene.ObjectType):
    average_category_price = graphene.Field(
        graphene.Float, category_id=graphene.ID(required=True)
    )

    @logged_in_user_required
    def resolve_average_category_price(root, info, category_id):
        products = Product.objects.get_object_by_public_id(category_id)
        if not products.exists():
            return None
        return products.aggregate(Avg("price"))["price__avg"]
