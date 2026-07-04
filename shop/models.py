from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=500)
    category = models.CharField(max_length=50, default="")
    sub_category = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    publish_date = models.DateField()
    product_image = models.ImageField(upload_to="shop/product", default="")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    helps = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address1 = models.TextField()
    address2 = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField(max_length=6)
    total_amount = models.IntegerField()
    payment_method = models.CharField(max_length=50, default="COD")
    order_status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
