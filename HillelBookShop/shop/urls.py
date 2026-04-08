from django.urls import path
from .views import ProductDetailView, ProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='shop'),
    path('product-detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail')
]
