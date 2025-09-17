from typing import Type
from django.db import models
from core.models.abstract import AuditIdentifierMixin, AuditIdentifierManager


class CategoryModelManager(AuditIdentifierManager):
    pass


class Category(AuditIdentifierMixin):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        blank=False,
        null=False,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=False, null=False)
    objects: Type[CategoryModelManager] = CategoryModelManager()

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name
