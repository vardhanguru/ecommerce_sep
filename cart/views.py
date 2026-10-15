from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Products
# Create your views here.
from django.shortcuts import get_object_or_404


@login_required
@require_POST
def add_to_cart(request, product_id):

    # what is the first step here??
    # check the product is available or not
    product = get_object_or_404(Products, id=product_id, is_available=True)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart_count = sum(CartItem.objects.filter(cart=cart).values_list('quantity', flat=True))
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'product_name': product.product_name,
            'cart_count': cart_count
        })

    messages.success(request, f"{product.product_name} added to your cart.", extra_tags='cart-added')
    return redirect('view_cart')

@login_required
def view_cart(request):

    cart, created = Cart.objects.get_or_create(user=request.user)

    

    cart_items = CartItem.objects.filter(cart=cart)
    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': sum(item.quantity for item in cart_items)
    }

    return render(request, 'cart/view_cart.html', context=context)

@login_required
@require_POST
def remove_cart_item(request, item_id):

    cart_item = get_object_or_404(
        CartItem, id=item_id
    )

    cart_item.delete()

    return redirect('view_cart')

@login_required
@require_POST
def remove_all_cart_items(request):

    cart = get_object_or_404(Cart, user=request.user)
    cart.delete()

    return redirect('product_list')

@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.quantity>0:
        cart_item.quantity -= 1
        if cart_item.quantity==0:
            cart_item.delete()
        else:
            cart_item.save()
    
    return redirect('view_cart')
