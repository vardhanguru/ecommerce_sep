import uuid
from decimal import Decimal

import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from cart.models import Cart, CartItem
from .forms import CheckoutForm
from .models import Order, OrderItem
from accounts.models import User


def get_razorpay_client():
    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )


def remove_ordered_items_from_cart(order):
    for order_item in order.orderitem_set.all():
        remaining_quantity = order_item.quantity
        cart_items = CartItem.objects.filter(
            cart__user=order.user,
            product=order_item.product,
        ).order_by("pk")

        for cart_item in cart_items:
            removed_quantity = min(cart_item.quantity, remaining_quantity)
            remaining_quantity -= removed_quantity
            cart_item.quantity -= removed_quantity
            if cart_item.quantity:
                cart_item.save(update_fields=["quantity"])
            else:
                cart_item.delete()
            if not remaining_quantity:
                break


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = list(
        CartItem.objects.filter(cart=cart).select_related("product")
    )
    total = sum(
        (item.product.price * item.quantity for item in cart_items),
        Decimal("0.00"),
    
    )
    print(request.user)
    user = User.objects.get(username=request.user)
    print(user)
    print(user.phone_number)
    print(user.address)
    print('--------------------------')
    form = CheckoutForm(
        request.POST if request.method == "POST" else None,
        initial={
            "name": request.user,
            "phone_number": user.phone_number,
            "address": user.address or "",
        },
    )

    if request.method == "POST":
        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect("view_cart")

        if form.is_valid():
            for item in cart_items:
                if not item.product.is_available or item.quantity > item.product.quantity:
                    messages.error(
                        request,
                        f"There is not enough stock for {item.product.product_name}.",
                    )
                    return redirect("view_cart")

            data = form.cleaned_data
            payment_method = data["payment_method"]
            gateway_order = None

            if payment_method == "ONLINE":
                try:
                    gateway_order = get_razorpay_client().order.create({
                        "amount": int(total * 100),
                        "currency": "INR",
                        "receipt": f"u{request.user.pk}-{uuid.uuid4().hex[:20]}",
                    })
                except Exception:
                    messages.error(
                        request,
                        "Online payment could not be started. Please try again.",
                    )
                    return redirect("checkout")

            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    name=data["name"],
                    phone_number=data["phone_number"],
                    total_amount=total,
                    payment_method=payment_method,
                    payment_status="Pending",
                    address=data["address"],
                    delivery_status="Shipped",
                    razorpay_order_id=gateway_order["id"] if gateway_order else None,
                )
                OrderItem.objects.bulk_create([
                    OrderItem(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price,
                    )
                    for item in cart_items
                ])

                if payment_method == "COD":
                    for item in cart_items:
                        item.product.quantity -= item.quantity
                        item.product.save(update_fields=["quantity"])
                    remove_ordered_items_from_cart(order)
                    return redirect("order_success", order_id=order.pk)

            return render(request, "payment.html", {
                "order": order,
                "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                "razorpay_amount": int(total * 100),
            })

    return render(request, "checkout.html", {
        "form": form,
        "cart_items": cart_items,
        "total_amount": total,
    })


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, "order_success.html", {"order": order})


@require_POST
def verify_payment(request):
    payment_data = {
        "razorpay_order_id": request.POST.get("razorpay_order_id", ""),
        "razorpay_payment_id": request.POST.get("razorpay_payment_id", ""),
        "razorpay_signature": request.POST.get("razorpay_signature", ""),
    }
    order = get_object_or_404(
        Order,
        razorpay_order_id=payment_data["razorpay_order_id"],
        payment_method="ONLINE",
    )

    try:
        get_razorpay_client().utility.verify_payment_signature(payment_data)
        with transaction.atomic():
            order = Order.objects.select_for_update().get(pk=order.pk)
            if order.payment_status != "Success":
                order.payment_status = "Success"
                order.razorpay_payment_id = payment_data["razorpay_payment_id"]
                order.razorpay_signature = payment_data["razorpay_signature"]
                order.save(update_fields=[
                    "payment_status",
                    "razorpay_payment_id",
                    "razorpay_signature",
                    "updated_at",
                ])
                for item in order.orderitem_set.select_related("product"):
                    item.product.quantity -= item.quantity
                    item.product.save(update_fields=["quantity"])
                remove_ordered_items_from_cart(order)
        success = True
        message = "Your payment was verified and your order is confirmed."
    except Exception:
        success = False
        message = "Payment verification failed. Your cart has not been cleared."

    return render(request, "result.html", {
        "success": success,
        "message": message,
        "payment_id": payment_data["razorpay_payment_id"] if success else "",
        "order": order,
    })

@login_required
def fetch_all_orders(request):
    orders = (
        Order.objects.filter(user=request.user)
        .order_by("-created_at")
    )
    return render(request, "orders.html", {"orders": orders})
