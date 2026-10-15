from django.contrib import admin
from django.urls import include, path

from accounts.views import home_view

urlpatterns = [
    path("", home_view, name="storefront_home"),
    path("admin/", admin.site.urls),
    path("products/", include("products.urls")),
    path("accounts/", include("accounts.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
]