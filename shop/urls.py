from django.urls import path
from . import views

urlpatterns = [
    path("", views.shophome, name="shopHome"),
    path("about-us/", views.about, name="about"),
    path("contact-us/", views.contact, name="contact"),
    path("tracker/", views.tracking, name="tracking_status"),
    path("search/", views.search, name="search"),
    path("product-details/<int:product_id>/", views.productview, name="product_details"),
    path("checkout/", views.checkout, name="checkout"),
    path("cart/", views.cart, name="cart"),
    path("order-success/", views.order_success, name="order_success"),

    # APIs
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("update-cart/", views.update_cart, name="update_cart"),
    path("get-cart/", views.get_cart, name="get_cart"),
]