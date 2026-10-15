from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from .models import Products
from .forms import ProductForm
from cart.models import CartItem


def product_create(request):

    form = ProductForm()
    data = {'form': form}

    if request.method == 'POST':

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('product_list')

    return render(request, 'products/product_create.html', context=data)


def product_list(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('search', '')
    print(category_id)
    print(category_id)
    print(search_query)
    if category_id:
        products_list = Products.objects.filter(Category=category_id)
    elif search_query:
        
        products_list = Products.objects.filter(product_name__icontains=search_query)
        print(products_list)
    else: 


        products_list = Products.objects.all()
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = sum(
            CartItem.objects.filter(cart__user=request.user).values_list('quantity', flat=True)
        )
    data = {'products_list': products_list, 'cart_count': cart_count}

    return render(request, 'products/products.html', context=data)


def product_update(request, pk):

    # fetch the product based on the pk
    product = Products.objects.get(pk=pk)  # what is the disadvantange of using get methid??
    product = get_object_or_404(Products, pk=pk)  # this is the better way to fetch the product based on the pk

    if request.method == 'POST':

        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect('product_list')

    form = ProductForm(instance=product)


    data = {'form': form}

    return render(request, 'products/product_update.html', context=data)


def product_details(request, pk):
    
    # fetch the product details
    product = get_object_or_404(Products, pk=pk)

    data = {'product': product}

    return render(request, 'products/product_details.html', context=data)


def product_delete(request, pk):

    product = get_object_or_404(Products, pk=pk)

    if request.method == 'POST':
        product.delete()

    return redirect('product_list')