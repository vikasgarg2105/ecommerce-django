from django.http import HttpResponse
from django.shortcuts import render

from .models import Product


# Create your views here.
def shophome(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    return render(request, 'shop/index.html')

def tracking(request):
    return render(request, 'shop/index.html')

def search(request):
    return render(request, 'shop/index.html')

def productview(request):
    return render(request, 'shop/index.html')

def checkout(request):
    return render(request, 'shop/index.html')