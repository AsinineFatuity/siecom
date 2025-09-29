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
