import pytest
from core.graphql.product.feedback import ProductFeedback
from core.tests.gql_queries import product as product_queries
from core.tests.utils import faker_factory


def create_product_inputs():
    return [
        {
            "name": "Note 10",
            "description": faker_factory.sentence(),
            "price": 50500,
            "stock": 10,
        },
        {
            "name": "Note 20 Ultra",
            "description": faker_factory.sentence(),
            "price": 119500,
            "stock": 15,
        },
        {
            "name": "S23 Ultra",
            "description": faker_factory.sentence(),
            "price": 93000,
            "stock": 20,
        },
    ]


def create_category_inputs():
    return [
        {"name": "Electronics", "description": faker_factory.sentence()},
        {"name": "Mobile Phones", "description": faker_factory.sentence()},
        {"name": "Smartphones", "description": faker_factory.sentence()},
        {"name": "Android", "description": faker_factory.sentence()},
        {"name": "Samsung", "description": faker_factory.sentence()},
    ]


INVALID_CREATE_PRODUCTS_TEST_CASES = {
    "duplicate_product_name": {
        "input": [
            {
                "name": "Note 10",
                "description": faker_factory.sentence(),
                "price": 50500,
                "stock": 10,
            }
            for _ in range(2)
        ],
        "expected_error": ProductFeedback.DUPLICATE_PRODUCT_NAME,
    },
    "duplicate_category_name": {
        "input": [
            {"name": "Electronics", "description": faker_factory.sentence()}
            for _ in range(2)
        ],
        "expected_error": ProductFeedback.DUPLICATE_CATEGORY_NAME,
    },
}


@pytest.mark.only
@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_case",
    INVALID_CREATE_PRODUCTS_TEST_CASES.values(),
    ids=INVALID_CREATE_PRODUCTS_TEST_CASES.keys(),
)
def test_create_product_invalid_inputs(authenticated_client, test_case, request):
    """
    Test creating products with invalid inputs.
    """
    test_id = request.node.name
    categories_input = (
        test_case["input"]
        if "duplicate_category_name" in test_id
        else create_category_inputs()
    )
    products_input = (
        test_case["input"]
        if "duplicate_product_name" in test_id
        else create_product_inputs()
    )
    response = authenticated_client.execute(
        product_queries.create_product_mutation(),
        variable_values={
            "products": products_input,
            "categories": categories_input,
        },
    )
    assert "errors" not in response
    data = response["data"]["createProduct"]
    assert not data["success"]
    assert data["message"] == test_case["expected_error"]
    assert len(data["createdProducts"]) == 0
