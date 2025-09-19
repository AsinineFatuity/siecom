from typing import Type, List, TYPE_CHECKING
from django.db import models
from django.db.models.functions import Lower
from tree_queries.models import TreeNode
from core.models.abstract import AuditIdentifierMixin, AuditIdentifierManager

if TYPE_CHECKING:
    # NOTE: Solving circular import for type checking only
    from core.graphql.product.types import CategoryInputType


class CategoryModelManager(AuditIdentifierManager):
    pass


class Category(AuditIdentifierMixin, TreeNode):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=False, null=False)
    objects: Type[CategoryModelManager] = CategoryModelManager()

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        constraints = [
            models.UniqueConstraint(Lower("name"), name="unique_category_name_ci")
        ]

    def __str__(self) -> str:
        return self.name

    @classmethod
    def create_category_hierarchy(
        cls, categories: List["CategoryInputType"]
    ) -> "Category":
        """
        Create or get a hierarchy of categories based on the provided list.
        The last item in the list is considered the most specific category.
        """
        db_categories = cls.objects.filter(
            name__in=[ci.name.lower() for ci in categories]
        )
        cat_name_obj_dict = {cat.name.lower(): cat for cat in db_categories}

        parent = None
        for category_input in categories:
            name_lower = category_input.name.lower()
            category = cat_name_obj_dict.get(name_lower)
            if not category:
                category, created = cls.objects.get_or_create(
                    name=name_lower,
                    defaults={
                        "description": category_input.description,
                        "parent": parent,
                    },
                )
                # avoid duplicated categories in the same hierarchy creation
                cat_name_obj_dict[name_lower] = category
            parent = category
        return cls.objects.select_related("parent").get(id=parent.id)
