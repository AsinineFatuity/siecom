from typing import Type
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from core.models.abstract import AuditIdentifierMixin, AuditIdentifierManager


class UserModelManager(UserManager, AuditIdentifierManager):
    pass


class User(AbstractUser, AuditIdentifierMixin):
    """
    NOTE: These are also referred to as "customers" when dealing with orders.
    """

    oidc_subject = models.CharField(max_length=255, default="", db_index=True)
    oidc_issuer = models.URLField(default="")
    email = models.EmailField(db_index=True, unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    objects: Type[UserModelManager] = UserModelManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    REQUIRED_USER_ATTRIBUTES = {
        "email",
        "first_name",
        "last_name",
        "oidc_subject",
        "oidc_issuer",
    }

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self) -> str:
        return self.email

    @classmethod
    def create_new_user(cls, **kwargs) -> "User":
        for key in kwargs.keys():
            if key not in cls.REQUIRED_USER_ATTRIBUTES:
                raise ValueError(f"Invalid attribute: {key}")
        kwargs["username"] = kwargs.get("email").split("@")[0]
        return cls.objects.create(**kwargs)

    @classmethod
    def update_existing_user(cls, user: "User", **kwargs) -> "User":
        for key in kwargs.keys():
            if key not in cls.REQUIRED_USER_ATTRIBUTES:
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, kwargs[key])
        user.save()
        return user
