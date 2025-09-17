import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


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


class AuditIdentifierMixin(models.Model):
    public_id = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True