from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length = 15, blank = True)
    profile_image = models.ImageField(upload_to="users/profile", blank=True, null=True)

    def __str__(self):
        return self.username