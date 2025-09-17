from typing import Type
from django.db import models
from core.models.abstract import AuditIdentifierMixin, AuditIdentifierManager
from core.models.category import Category


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

    def __str__(self) -> str:
        return self.name
