from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect

from shop.cart.cart import Cart
from shop.models import Product


def cart_detail(request):
    """Render the current shopping cart and calculated total."""
    cart = Cart(request)

    context = {
        'cart': cart,
        'total_price': cart.get_total_price()
    }
    return render(request, 'shop/cart/pages/page-cart.html', context)


def cart_add(request, product_id):
    """Add a product to the cart or increase its quantity."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product=product, quantity=quantity, override_quantity=False)
        messages.success(request, f'{product.name} added to cart')
    return redirect('cart_detail')


def cart_remove(request, product_id):
    """Remove a product from the cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart.remove(product)
    messages.info(request, f'{product.name} видалено з кошика')
    return redirect('cart_detail')


def cart_update(request, product_id):
    """Update the quantity of a product already stored in the cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product=product, quantity=quantity, override_quantity=True)

    return redirect('cart_detail')


def cart_clear(request):
    """Remove every item from the current session cart."""
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')
