
from django.urls import path, include
from .views import add_to_cart, view_cart, remove_cart_item, remove_all_cart_items, increase_quantity, decrease_quantity

urlpatterns = [
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('view_cart/', view_cart, name='view_cart'),
    path('remove-cart/<int:item_id>/', remove_cart_item, name='remove_cart_item'),
    path('remove-all-items/', remove_all_cart_items, name='remove_all_cart_items'),
    path('increase_quantity/<int:item_id>', increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>', decrease_quantity, name='decrease_quantity'),
]