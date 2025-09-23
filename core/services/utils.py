from django.template.loader import render_to_string
from core.models import Order


class AlertUtils:
    @staticmethod
    def create_order_confirmation_sms_alert(name: str, order_id: int) -> str:
        return f"Hello {name}, your order with ID {order_id} has been successfully placed. Thank you for shopping with us!"

    @staticmethod
    def create_order_confirmation_email_alert(order: Order) -> str:
        context = {
            "customer_name": order.user.get_full_name(),
            "order_id": order.id,
            "product_name": order.product.name,
            "quantity": order.quantity,
            "price": order.total_price,
            "address": f"{order.address.street}, {order.address.city}",
            "phone": order.address.formatted_phone_number,
            "email": order.user.email,
            "now": order.created_at,
        }
        return render_to_string("email.html", context)
