from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
import json
from .utils import get_cart_products

from .models import Product, Contact


# Create your views here.
def shophome(request):
    cart = request.session.get("cart", {})

    allProduct = []
    catProducts = Product.objects.values('category', 'product_id')
    categories = {item['category'] for item in catProducts}
    for category in categories:
        products = Product.objects.filter(category = category)

        for product in products:
            product_id = str(product.product_id)

            if product_id in cart:
                product.cart_quantity = cart[product_id]
            else:
                product.cart_quantity = 0
        
        allProduct.append({
        'category': category,
        'products': products
    })

    print(allProduct)
    context = {'products': allProduct}
    return render(request, 'shop/index.html', context)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        helps = request.POST.get('help', '')

        contact_details = Contact(name = name, email = email, phone = phone, helps = helps)
        contact_details.save()
        
    return render(request, 'shop/contact.html')

def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = str(data.get("product_id"))

        cart = request.session.get("cart", {})

        if(product_id in cart):
            cart[product_id] += 1
        else:
            cart[product_id] = 1

        request.session["cart"] = cart

        cart_products = get_cart_products(cart)

        cart_html = render_to_string(
            "shop/components/cart-items.html",{"cart_products" : cart_products}
        )

        total_items = sum(cart.values())
        return JsonResponse({
            "status" : "Success",
            "cart_html" : cart_html,
            "quantity": cart[product_id],
            "cart_count" : total_items
        })

def update_cart(request):
    data = json.loads(request.body)
    
    product_id = str(data["product_id"])
    action = data["action"]

    cart = request.session.get("cart", {})

    deleted = False

    if action == "increase":
        cart[product_id] += 1
    elif action == "decrease":
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]
            deleted = True

    request.session["cart"] = cart

    cart_products = get_cart_products(cart)
    cart_html = render_to_string(
        "shop/components/cart-items.html", {"cart_products" : cart_products}
    )

    return JsonResponse({
        "quantity": cart.get(product_id, 0),
        "deleted": deleted,
        "cart_count": sum(cart.values()),
        "cart_html": cart_html
    })

def tracking(request):
    return render(request, 'shop/tracker.html')

def search(request):
    return render(request, 'shop/search.html')

def productview(request, product_id):
    product = Product.objects.get(product_id = product_id)
    context = {'product': product}
    return render(request, 'shop/product-details.html', context)

def checkout(request):
    return render(request, 'shop/checkout.html')