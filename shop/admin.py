from django.contrib import admin
from .models import Product, Contact, Order, OrderItem
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

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    show_change_link = True

    readonly_fields = (
        "product",
        "quantity",
        "price",
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "firstname",
        "lastname",
        "phone",
        "total_amount",
        "payment_method",
        "order_status",
        "created_at",
    )

    inlines = [OrderItemInline]