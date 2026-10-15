
from django.urls import path

from .views import checkout, order_success, verify_payment, fetch_all_orders

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("create/", checkout, name="create_payment"),
    path("success/", verify_payment, name="payment_success"),
    path("order-success/<int:order_id>/", order_success, name="order_success"),
    path('all-orders/', fetch_all_orders, name='fetch_all_orders'),
]

