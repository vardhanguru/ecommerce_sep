from django.db import models

# Create your models here.

class Category(models.Model):

    # fileds or columns required?

    name = models.CharField(max_length=20, unique=True)

    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='category/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    
    product_name = models.CharField(max_length=50)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)

    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)  # this is available at the time of product creation, it wont change at all

    image = models.ImageField(upload_to='products/', blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name



