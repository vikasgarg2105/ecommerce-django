from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
import json
from .utils import get_cart_products

from .models import Product, Contact, Order, OrderItem


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
    elif action == "remove":
        del cart[product_id]
        deleted = True

    request.session["cart"] = cart

    cart_products = get_cart_products(cart)
    cart_html = render_to_string(
        "shop/components/cart-items.html", {"cart_products" : cart_products}
    )
    total_price = 0
    for product in cart_products:
        total_price += product.subtotal

    return JsonResponse({
        "quantity": cart.get(product_id, 0),
        "deleted": deleted,
        "cart_count": sum(cart.values()),
        "cart_html": cart_html,
        "total_price": total_price,
        "is_empty": len(cart) == 0
    })

def get_cart(request):
    cart = request.session.get("cart", {})
    cart_products = get_cart_products(cart)

    cart_html = render_to_string("shop/components/cart-items.html", {"cart_products" : cart_products})

    return JsonResponse({
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

def cart(request):
    cart = request.session.get("cart", {})
    cart_products = []
    total_price = 0
    for product_id,qty in cart.items():
        product = Product.objects.get(product_id = product_id)
        product.quantity = qty
        product.subtotal = (product.price*qty)
        total_price += product.subtotal
        
        cart_products.append(product)

    context = {
        "cart_products": cart_products,
        "total_price" : total_price
    }

    return render(request, 'shop/cart.html', context)


def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("cart")

    cart_products = get_cart_products(cart)

    total_price = 0
    subtotal = sum(product.subtotal for product in cart_products)
    tax = 0
    shipping = 0
    total_price = subtotal + shipping + tax


    if request.method == "POST":
        firstname = request.POST.get("first_name", "").strip()
        lastname = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address1 = request.POST.get("address1", "").strip()
        address2 = request.POST.get("address2", "").strip()
        city = request.POST.get("city", "").strip()
        state = request.POST.get("state", "").strip()
        pincode = request.POST.get("pincode", "").strip()
        payment_method = request.POST.get("payment_method", "")
        accept = request.POST.get("accept", "")

        errors = {}
        if not firstname:
            errors["firstname"] = "First name is required"
        if not lastname:
            errors["lastname"] = "Last name is required"
        if not email:
            errors["email"] = "email is required"
        elif "@" and "." not in email:
            errors["email"] = "Invalid email."
        if not phone:
            errors["phone"] = "phone is required"
        elif not phone.isdigit():
            errors["phone"] = "Phone should contain only digits."
        elif len(phone) != 10:
            errors["phone"] = "Phone must be 10 digits."
        if not address1:
            errors["address1"] = "address1 is required"
        if not city:
            errors["city"] = "city is required"
        if not state:
            errors["state"] = "state is required"
        if not pincode:
            errors["pincode"] = "pincode is required"
        if payment_method not in ["COD", "UPI"]:
            errors["payment_method"] = "Select payment method."
        if not accept:
            errors["accept"] = "Please accept Terms & Conditions."

        if errors:
            context = {
                "cart_products": cart_products,
                "subtotal": subtotal,
                "shipping": shipping,
                "tax": tax,
                "total_price": total_price,
                "errors": errors,
            }
            return render(request, 'shop/checkout.html', context)


        order = Order.objects.create(
            firstname = firstname,
            lastname = lastname,
            email = email,
            phone = phone,
            address1 = address1,
            address2 = address2,
            city = city,
            state = state,
            pincode = pincode,
            total_amount = 0,
            payment_method=payment_method,
        )

        for product in cart_products:

            OrderItem.objects.create(
                order = order,
                product = product,
                quantity = product.quantity,
                price = product.price
            )

        order.total_amount = total_price
        order.save()

        request.session["cart"] = {}
        request.session["last_order_id"] = order.order_id
        return redirect("order_success", order_id=order.order_id)

    context = {
        "cart_products": cart_products,
        "subtotal": subtotal,
        "shipping": shipping,
        "tax": tax,
        "total_price": total_price,
    }

    return render(request, 'shop/checkout.html', context)

def order_success(request, order_id):

    order_id = request.session.get("last_order_id")

    if not order_id:
        return redirect("shopHome")

    order = get_object_or_404(Order, order_id=order_id)

    context = {
        "order": order
    }

    return render(
        request,
        "shop/success.html",
        context
    )

def order_details(request, order_id):
    last_order_id = request.session.get("last_order_id")

    if last_order_id != order_id:
        return redirect("shopHome")
        
    order = get_object_or_404(Order, order_id = order_id)
    order_items = OrderItem.objects.filter(order = order)

    context = {
       "order": order,
       "order_items": order_items
    }

    return render(request, "shop/order-details.html", context)