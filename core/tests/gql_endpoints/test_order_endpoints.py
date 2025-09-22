import pytest
from unittest.mock import patch
from uuid import uuid4
from core.tests.factory import ProductFactory
from core.tests.gql_queries import order as order_queries
from core.tests.utils import generate_phone_with_country_code, faker_factory
from core.graphql.order.feedback import OrderFeedback


def generate_address():
    return {
        "phoneNumber": generate_phone_with_country_code(),
        "street": faker_factory.street_address(),
        "city": faker_factory.city(),
    }


INVALID_ORDER_TEST_CASES = {
    "invalid_product_id": {
        "product_id": str(uuid4()),
        "quantity": 1,
        "address": generate_address(),
        "expected_message": OrderFeedback.PRODUCT_DOES_NOT_EXIST,
    },
    "invalid_product_quantity": {
        "product_id": None,
        "quantity": -5,
        "address": generate_address(),
        "expected_message": OrderFeedback.INVALID_PRODUCT_QUANTITY,
    },
    "invalid_phone_number": {
        "product_id": None,
        "quantity": 1,
        "address": {
            "phoneNumber": "12345",
            "street": faker_factory.street_address(),
            "city": faker_factory.city(),
        },
        "expected_message": OrderFeedback.INVALID_PHONE_NUMBER,
    },
}


@pytest.mark.parametrize(
    "test_case", INVALID_ORDER_TEST_CASES.values(), ids=INVALID_ORDER_TEST_CASES.keys()
)
def test_invalid_inputs_provided(authenticated_client, db, test_case, request):
    test_id = request.node.callspec.id
    require_valid_product = ["invalid_product_quantity", "invalid_phone_number"]
    if test_id in require_valid_product:
        product = ProductFactory.create()
        test_case["product_id"] = product.public_id
    response = authenticated_client.execute(
        order_queries.create_order_mutation(
            test_case["product_id"], test_case["quantity"]
        ),
        variable_values={
            "address": test_case["address"],
        },
    )
    assert "errors" not in response
    data = response["data"]["createOrder"]
    assert data["success"] is False
    assert data["message"] == test_case["expected_message"]
    assert data["order"] is None


@patch("core.graphql.order.mutations.send_order_confirmation_email_to_admin")
@patch("core.graphql.order.mutations.send_order_confirmation_sms_to_customer")
def test_create_order_successfully(
    mock_send_sms, mock_send_email, authenticated_client, db
):
    product = ProductFactory.create(stock=10, price=100.00)
    address = generate_address()
    quantity = 2
    response = authenticated_client.execute(
        order_queries.create_order_mutation(product.public_id, quantity),
        variable_values={
            "address": address,
        },
    )
    assert "errors" not in response
    data = response["data"]["createOrder"]
    assert data["success"] is True
    assert data["message"] == OrderFeedback.ORDER_CREATION_SUCCESS
    order_data = data["order"]
    assert order_data is not None
    assert order_data["product"]["id"] == str(product.public_id)
    assert order_data["quantity"] == quantity
    assert float(order_data["totalPrice"]) == float(product.price * quantity)
    assert order_data["address"]["phoneNumber"] == address["phoneNumber"]
    assert order_data["address"]["street"] == address["street"]
    assert order_data["address"]["city"] == address["city"]
    product.refresh_from_db()
    assert product.stock == 8
    created_order = product.orders.first()
    assert created_order is not None
    mock_send_email.schedule.assert_called_once()
    mock_send_email.schedule.assert_called_with(args=(created_order.id,))
    mock_send_sms.schedule.assert_called_once()
    mock_send_sms.schedule.assert_called_with(args=(created_order.id,))
