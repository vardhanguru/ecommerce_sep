
from django import forms

# first import the model
from .models import Products

class ProductForm(forms.ModelForm):

    class Meta:
        model = Products

        fields = ['Category', 'product_name', 'description', 'price', 'quantity', 'image', 'is_available']