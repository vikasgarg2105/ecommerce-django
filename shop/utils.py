from .models import Product

def get_cart_products(cart):
    cart_products = []
    
    for product_id, quantity in cart.items():
        product = Product.objects.get(product_id = product_id)

        product.quantity = quantity
        product.subtotal = product.price * quantity
        cart_products.append(product)
    return cart_products