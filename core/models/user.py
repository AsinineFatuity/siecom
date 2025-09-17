from typing import Type
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from core.models.abstract import AuditIdentifierMixin, AuditIdentifierManager


class UserModelManager(UserManager, AuditIdentifierManager):
    pass


class User(AbstractUser, AuditIdentifierMixin):
    auth0_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    objects: Type[UserModelManager] = UserModelManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self) -> str:
        return self.email
