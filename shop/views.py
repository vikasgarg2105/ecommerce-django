from django.http import HttpResponse
from django.shortcuts import render

from .models import Product, Contact


# Create your views here.
def shophome(request):
    products = Product.objects.all()

    allProduct = []
    catProducts = Product.objects.values('category', 'product_id')
    categories = {item['category'] for item in catProducts}
    for category in categories:
        product = Product.objects.filter(category = category)
        allProduct.append({
        'category': category,
        'products': product
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