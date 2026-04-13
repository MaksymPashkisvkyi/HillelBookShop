from django.urls import path
from .views import ProductDetailView, ProductListView
from .cart.views import cart_detail, cart_add, cart_remove, cart_update, cart_clear
from .orders.views import order_create

urlpatterns = [
    path('', ProductListView.as_view(), name='shop'),
    path('product-detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>', cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>', cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', cart_update, name='cart_update'),
    path('cart/cleare/', cart_clear, name='cart_clear'),
    path('order/create/', order_create, name='order_create'),
]
