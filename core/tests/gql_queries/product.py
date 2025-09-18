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
