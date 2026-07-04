from django.contrib import admin
from .models import Product, Contact, Order
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'product_name',
        'category',
    ]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        'contact_id',
        'name'
    ]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_id',
        'full_name',
        'order_status'
    ]