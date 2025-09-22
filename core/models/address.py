from typing import Type
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from core.models.abstract import AuditIdentifierMixin, AuditIdentifierManager
from core.models.user import User


class AddressModelManager(AuditIdentifierManager):
    pass


class Address(AuditIdentifierMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    phone_number = PhoneNumberField(null=False, blank=False)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    objects: Type[AddressModelManager] = AddressModelManager()

    class Meta:
        verbose_name = "address"
        verbose_name_plural = "addresses"

    def __str__(self) -> str:
        return f"{self.street}, {self.city}, {self.user.email}"

    @classmethod
    def create_address(
        cls, user_id: int, phone_number: str, street: str, city: str
    ) -> "Address":
        address = cls.objects.select_related("user").create(
            user_id=user_id, phone_number=phone_number, street=street, city=city
        )
        return address
