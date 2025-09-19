import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from tree_queries.query import TreeQuerySet


class AuditIdentifierQuerySet(models.QuerySet):
    def get_object_by_public_id(self, public_id: str):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return None


class AuditIdentifierManager(models.Manager):
    def get_queryset(self):
        return AuditIdentifierQuerySet(self.model, using=self._db)

    def get_object_by_public_id(self, public_id: str):
        return self.get_queryset().get_object_by_public_id(public_id)


class CustomTreeQueryset(AuditIdentifierQuerySet, TreeQuerySet):
    pass


class CustomTreeManager(models.Manager.from_queryset(CustomTreeQueryset)):
    """NOTE: This approach of combining multiple QuerySet classes is warranted by the need to have both:
    1. Pass through methods from AuditIdentifierQuerySet (e.g., get_object_by_public_id)
    2. TreeQuerySet functionalities (e.g., tree_filter, order_siblings_by)
    To have done just a simple multiple inheritance of QuerySet (without models.Manager.from_queryset(...)) classes would not have worked as expected.
    Inspired by https://docs.djangoproject.com/en/5.2/topics/db/managers/#from-queryset
    """

    pass


class AuditIdentifierMixin(models.Model):
    public_id = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
