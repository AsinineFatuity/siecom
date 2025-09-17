from typing import Type
from django.db import models
from core.models.abstract import AuditIdentifierMixin, AuditIdentifierManager
from core.models.user import User
from core.models.product import Product
from core.models.address import Address


class OrderModelManager(AuditIdentifierManager):
    pass


class Order(AuditIdentifierMixin):
    # order statuses
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    ALL_STATUSES = [PENDING, SHIPPED, DELIVERED, CANCELLED]
    status_choices = [(status, status.capitalize()) for status in ALL_STATUSES]
    # payment methods
    CREDIT_CARD = "credit_card"
    MPESA = "mpesa"
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    BANK_CHEQUE = "bank_cheque"
    OTHER = "other"
    ALL_PAYMENT_METHODS = [CREDIT_CARD, MPESA, CASH, BANK_TRANSFER, BANK_CHEQUE, OTHER]
    payment_method_choices = [
        (method, method.replace("_", " ").capitalize())
        for method in ALL_PAYMENT_METHODS
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        blank=False,
        null=False,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders",
        blank=False,
        null=False,
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name="orders",
        blank=False,
        null=False,
    )
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=status_choices, default=PENDING)
    payment_method = models.CharField(
        max_length=50, choices=payment_method_choices, default=CASH
    )
    is_paid = models.BooleanField(default=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    objects: Type[OrderModelManager] = OrderModelManager()

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"

    def __str__(self) -> str:
        return f"Order {self.id} by {self.user.email}"
