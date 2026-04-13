from django.contrib import messages
from django.shortcuts import redirect, render

from shop.cart.cart import Cart
from shop.models import Customer
from shop.orders.forms import OrderCreateForm
from shop.orders.models import OrderItem


def order_create(request):
    cart = Cart(request)

    if not cart.cart:
        messages.warning(request, 'Ваш кошик пустий!')
        return redirect('cart_detail')
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = cart.get_total_price()
            if request.user.is_authenticated:
                try:
                    order.customer = request.user.customer
                except:
                    customer, created = Customer.objects.get_or_create(user=request.user)
                    order.customer = customer
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()

            messages.success(request, f'Замовлення №{order.id} було успішно оформлено')
            return render(request, 'shop/orders/pages/page-success-order.html', {'order': order})
    else:
        initial = {}
        if request.user.is_authenticated:
            customer = None
            user = request.user

            initial = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone,
            }
            if hasattr(user, 'customer'):
                customer = user.customer
            if customer:
                initial.update({
                    'address': getattr(customer, 'address', ''),
                })

        form = OrderCreateForm(initial=initial)

    context = {
        'form': form,
        'cart': cart,
        'total_price': cart.get_total_price(),
    }

    return render(request, 'shop/orders/pages/page-create-order.html', context)
