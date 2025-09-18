import decimal
from typing import Type, List, TYPE_CHECKING
from django.db import models
from django.db.models.functions import Lower
from core.models.abstract import AuditIdentifierMixin, AuditIdentifierManager
from core.models.category import Category

if TYPE_CHECKING:
    from core.graphql.product.types import ProductInputType


class ProductModelManager(AuditIdentifierManager):
    pass


class Product(AuditIdentifierMixin):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        blank=False,
        null=False,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    objects: Type[ProductModelManager] = ProductModelManager()

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        constraints = [
            models.UniqueConstraint(Lower("name"), name="unique_product_name_ci")
        ]

    def __str__(self) -> str:
        return self.name

    @classmethod
    def create_products(
        cls, product_inputs: List["ProductInputType"], category: Category
    ) -> List["Product"]:
        db_products = cls.objects.filter(
            name__in=[pi.name.lower() for pi in product_inputs],
            category_id=category.id,
        )
        prod_name_obj_dict = {prod.name.lower(): prod for prod in db_products}
        to_create = []

        for product_input in product_inputs:
            if product_input.name.lower() not in prod_name_obj_dict:
                to_create.append(
                    cls(
                        name=product_input.name.lower(),
                        description=product_input.description,
                        price=decimal.Decimal(product_input.price),
                        stock=product_input.stock,
                        category_id=category.id,
                    )
                )
        return cls.objects.select_related("category").bulk_create(to_create)
