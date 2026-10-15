from django.db import models

from products.models import Products
from accounts.models import User
# Create your models here.

class Cart(models.Model):

    # columns required for the cart???
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s cart"

class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    product = models.ForeignKey(Products,on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)