from typing import Type
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from core.models.abstract import AuditIdentifierMixin, AuditIdentifierManager


class UserModelManager(UserManager, AuditIdentifierManager):
    pass


class User(AbstractUser, AuditIdentifierMixin):
    """
    NOTE: These are also referred to as "customers" when dealing with orders.
    """

    oidc_subject = models.CharField(max_length=255, default="")
    oidc_issuer = models.URLField(default="")
    email = models.EmailField(
        unique=True
    )  # NOTE:though often queried by username, django adds index for unique constraint
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
        indexes = [
            models.Index(
                fields=["oidc_subject", "email"], name="oidc_subject_email_idx"
            ),
        ]

    def __str__(self) -> str:
        return self.email

    @classmethod
    def create_or_update_user(cls, **user_info) -> "User":
        for key in user_info.keys():
            if key not in cls.REQUIRED_USER_ATTRIBUTES:
                raise ValueError(f"Invalid attribute: {key}")
        existing_user = cls.objects.filter(
            oidc_subject=user_info.get("oidc_subject"),
            email=user_info.get("email"),
        ).first()
        if existing_user:
            return cls._update_existing_user(existing_user, **user_info)
        return cls._create_new_user(**user_info)

    @classmethod
    def _create_new_user(cls, **user_info) -> "User":
        user_info["username"] = user_info.get("email").split("@")[0]
        return cls.objects.create(**user_info)

    @classmethod
    def _update_existing_user(cls, user: "User", **user_info) -> "User":
        for key in user_info.keys():
            setattr(user, key, user_info[key])
        user.save()
        return user
