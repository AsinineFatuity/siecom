import pytest
from core.graphql.product.feedback import ProductFeedback
from core.tests.gql_queries import product as product_queries
from core.tests.utils import faker_factory
from core.models import Product, Category


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


@pytest.mark.parametrize(
    "test_case",
    INVALID_CREATE_PRODUCTS_TEST_CASES.values(),
    ids=INVALID_CREATE_PRODUCTS_TEST_CASES.keys(),
)
def test_create_product_invalid_inputs(authenticated_client, test_case, request, db):
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


@pytest.fixture
def created_products(authenticated_client, db):
    products_input = create_product_inputs()
    categories_input = create_category_inputs()
    response = authenticated_client.execute(
        product_queries.create_product_mutation(),
        variable_values={
            "products": products_input,
            "categories": categories_input,
        },
    )
    assert "errors" not in response
    data = response["data"]["createProduct"]
    assert data["success"]
    assert data["message"] == ProductFeedback.PRODUCT_CREATION_SUCCESS
    assert len(data["createdProducts"]) == len(products_input)
    created_product_names = [p["name"] for p in data["createdProducts"]]
    for product in products_input:
        assert product["name"].lower() in created_product_names
    all_products = Product.objects.all()
    assert all_products.count() == len(products_input)
    all_categories = Category.objects.all()
    assert all_categories.count() == len(categories_input)
    return data["createdProducts"]


def test_create_product_valid_inputs(created_products):
    """
    Test creating products with valid inputs.
    """
    for product in created_products:
        assert product["category"]["name"].lower() == "samsung"
        assert product["category"]["parent"]["name"].lower() == "android"


def test_calculate_average_price_per_category(
    authenticated_client, created_products, db
):
    """
    Test calculating average price per category.
    """
    electronics_category = Category.objects.get(name__iexact="Electronics")
    expected_average_price = sum(
        [float(product["price"]) for product in created_products]
    ) / len(created_products)
    expected_average_price = round(expected_average_price, 2)
    response = authenticated_client.execute(
        product_queries.calculate_average_price_query(electronics_category.public_id)
    )
    assert "errors" not in response
    data = response["data"]["averagePricePerCategory"]
    assert data["category"]["id"] == str(electronics_category.public_id)
    assert data["averagePrice"] == expected_average_price
    assert data["success"]
    assert data["message"] == ProductFeedback.AVERAGE_PRICE_CALCULATION_SUCCESS
