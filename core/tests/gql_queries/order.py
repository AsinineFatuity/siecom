def create_order_mutation(product_id: str, quantity: int):
    return """mutation($address: AddressInputType!) {
        createOrder(productId: "%s", quantity: %d, address: $address) {
            order {
                id
                product {
                    id
                    name
                    description
                    price
                    stock
                }
                quantity
                totalPrice
                status
                paymentMethod
                isPaid
                address {
                    id
                    street
                    city
                    phoneNumber
                }
                user {
                    id
                    email
                }
            }
            success
            message
        }
    }""" % (product_id, quantity)
