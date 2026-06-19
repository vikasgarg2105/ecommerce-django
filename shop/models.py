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
