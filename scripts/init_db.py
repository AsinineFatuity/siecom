import logging
from types import SimpleNamespace
from core.models import Category, Product


def get_samsung_product_inputs():
    return [
        {
            "name": "Note 10",
            "description": "Note 10 from Samsung",
            "price": 50500,
            "stock": 10,
        },
        {
            "name": "Note 20 Ultra",
            "description": "Note 20 Ultra from Samsung",
            "price": 119500,
            "stock": 15,
        },
        {
            "name": "S23 Ultra",
            "description": "S23 Ultra from Samsung",
            "price": 93000,
            "stock": 20,
        },
    ]


def get_samsung_category_inputs():
    return [
        {"name": "Electronics", "description": "Electronics category"},
        {"name": "Mobile Phones", "description": "Mobile Phones category"},
        {"name": "Smartphones", "description": "Smartphones category"},
        {"name": "Android", "description": "Android category"},
        {"name": "Samsung", "description": "Samsung category"},
    ]


def get_readmi_category_inputs():
    original_categories = get_samsung_category_inputs()
    # replace "Samsung" with Readmi
    original_categories[-1] = {
        "name": "Readmi",
        "description": "Readmi category",
    }
    return original_categories


def get_readmi_product_inputs():
    return [
        {
            "name": "A3X",
            "description": "A3X from Readmi",
            "price": 15000,
            "stock": 30,
        },
        {
            "name": "Note 13 Pro",
            "description": "Note 13 Pro from Readmi",
            "price": 52000,
            "stock": 25,
        },
    ]


def create_products():
    s_cat = get_samsung_category_inputs()
    s_prod = get_samsung_product_inputs()
    r_cat = get_readmi_category_inputs()
    r_prod = get_readmi_product_inputs()

    # Create typified inputs
    s_cat_inputs = [SimpleNamespace(**cat) for cat in s_cat]
    r_cat_inputs = [SimpleNamespace(**cat) for cat in r_cat]
    s_prod_inputs = [SimpleNamespace(**prod) for prod in s_prod]
    r_prod_inputs = [SimpleNamespace(**prod) for prod in r_prod]

    s_cat_id = Category.create_category_hierarchy(s_cat_inputs)
    r_cat_id = Category.create_category_hierarchy(r_cat_inputs)
    Product.create_products(s_prod_inputs, s_cat_id)
    Product.create_products(r_prod_inputs, r_cat_id)


def run():
    create_products()
    logging.info(f"{__name__}:Products and categories created successfully.")
