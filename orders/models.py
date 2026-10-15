from django.db import models

# Create your models here.
from products.models import Products

class Order(models.Model):

    payment_status_choices = [
        ('Pending','Pending'),
        ("Success","success"),
        ("Failed",'Failure')
    ]

    payment_choices = [
        ('COD', 'Cash On Delivery'),
        ("ONLINE",'Online Payment')
    ]

    delivery_choices = [
        ('Shipped', 'Shipper'),
        ('Out for delivery', 'Out for deliver'),
        ('Delivered', 'Delivered')
    ]

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

    name = models.CharField()

    address = models.TextField()
    phone_number = models.CharField()

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=payment_choices)
    payment_status = models.CharField(max_length=15, choices=payment_status_choices, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    delivery_status = models.CharField(max_length=35, choices=delivery_choices, default='Shipped')

    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_signature = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Order"

# todo - implement orderitems model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"
