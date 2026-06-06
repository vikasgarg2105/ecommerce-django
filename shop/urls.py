from django.urls import path
from . import views

urlpatterns = [
    path("", views.shophome, name="shopHome"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("tracker/", views.tracking, name="tracking_status"),
    path("search/", views.search, name="search"),
    path("product-details/", views.productview, name="product_details"),
    path("checkout/", views.checkout, name="checkout")
]