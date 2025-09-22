import graphene
import traceback
from phonenumbers import parse, is_valid_number
from core.models import Order, Address, Product
from siecom.decorators import logged_in_user_required
from core.graphql.order.types import OrderType, AddressInputType
from core.graphql.order.feedback import OrderFeedback


class CreateOrder(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)
        quantity = graphene.Int(required=True)
        address = AddressInputType(required=True)

    order = graphene.Field(OrderType)
    success = graphene.Boolean()
    message = graphene.String()

    @logged_in_user_required
    def mutate(root, info, product_id, quantity, address):
        user = info.context.user
        try:
            product = Product.objects.get_object_by_public_id(product_id)
            if not product:
                return CreateOrder(
                    success=False, message=OrderFeedback.PRODUCT_DOES_NOT_EXIST
                )
            if quantity <= 0 or quantity > product.stock:
                return CreateOrder(
                    success=False, message=OrderFeedback.INVALID_PRODUCT_QUANTITY
                )
            parsed_phone_number = parse(address.phone_number, "KE")
            if not is_valid_number(parsed_phone_number):
                return CreateOrder(
                    success=False, message=OrderFeedback.INVALID_PHONE_NUMBER
                )

            address_instance = Address.create_address(
                user_id=user.id,
                phone_number=address.phone_number,
                street=address.street,
                city=address.city,
            )
            order = Order.create_order(
                user_id=user.id,
                product_id=product.id,
                address_id=address_instance.id,
                quantity=quantity,
            )
            return CreateOrder(
                order=order, success=True, message=OrderFeedback.ORDER_CREATION_SUCCESS
            )

        except Exception:
            traceback.print_exc()
            return CreateOrder(
                success=False, message=OrderFeedback.ORDER_CREATION_FAILURE
            )


class OrderMutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
