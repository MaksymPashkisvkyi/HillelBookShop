from django.urls import path
from .views import DashboardView, ProductCreateView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('product-create/', ProductCreateView.as_view(), name='product_create'),
    path('product-update/<slug:slug>/', ProductUpdateView.as_view(), name='product_update'),
    path('product-delete/<slug:slug>/', ProductDeleteView.as_view(), name='product_delete'),
]
