def create_product_mutation():
    return """
    mutation($products: [ProductInputType!]!, $categories: [CategoryInputType!]!) {
        createProduct(products: $products, categories: $categories) {
            success
            message
            createdProducts {
                id
                name
                description
                price
                stock
                category {
                    id
                    name
                    parent {
                        id
                        name
                    }
                }
            }
        }
    }
    """


def calculate_average_price_query(category_id: str):
    return (
        """
    query {
        averagePricePerCategory(categoryId: "%s") {
            category {
                id
                name
            }
            averagePrice
            success
            message
        }
    }
    """
        % category_id
    )
