from django.db import models

# Create your models here.

# here, I'm not going to use the default user model

from django.contrib.auth.models import AbstractUser
# this abstract users provides us the features to use the existing columns and add extra columns as well

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True, null=True)
    seller_or_not = models.BooleanField(default=False)

    def __str__(self):
        return self.username
