from huey.contrib.djhuey import db_task
from core.models import Order
from core.services import EmailService, AlertUtils, SMSService


@db_task(retries=3, retry_delay=1800)
def send_order_confirmation_email_to_admin(order_id: int):
    order = Order.objects.select_related("user", "product", "address").get(id=order_id)
    email_body = AlertUtils.create_order_confirmation_email_alert(order)
    email_service = EmailService(
        recipients=[order.user.email],
        html_body=email_body,
    )
    email_service.send_emails()


@db_task(retries=3, retry_delay=1800)
def send_order_confirmation_sms_to_customer(order_id: int):
    order = Order.objects.select_related("user", "product", "address").get(id=order_id)
    sms_body = AlertUtils.create_order_confirmation_sms_alert(
        order.user.first_name, order.id
    )
    sms_service = SMSService(
        recipients=[order.address.formatted_phone_number],
        message=sms_body,
    )
    sms_service.send_sms()
