
from django.urls import path
from .views import product_create, product_list, product_update, product_details, product_delete

urlpatterns = [
    path('create/', product_create, name='product_create'),
    path('list/', product_list, name='product_list'),
    path('update/<int:pk>/', product_update, name='product_update'),
    path('details/<int:pk>/', product_details, name='product_details'),
    path('delete/<int:pk>/', product_delete, name='product_delete'),
]
