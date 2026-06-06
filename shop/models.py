from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="")
    sub_category = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    product_description = models.CharField(max_length=500)
    publish_date = models.DateField()
    product_image = models.ImageField(upload_to="shop/product", default="")

    def __str__(self):
        return self.product_name
