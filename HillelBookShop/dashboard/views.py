from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from shop.models import Product


class DashboardView(LoginRequiredMixin, ListView):
    queryset = Product.objects.all()
    template_name = 'dashboard/pages/page-dashboard.html'
    context_object_name = 'products'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    permission_required = 'shop.add_product'
    template_name = 'dashboard/pages/book-create.html'
    fields = '__all__'
    success_url = reverse_lazy('dashboard')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    permission_required = 'shop.change_product'
    template_name = 'dashboard/pages/book-update.html'
    fields = '__all__'
    success_url = reverse_lazy('dashboard')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    permission_required = 'shop.delete_product'
    template_name = 'dashboard/pages/book-delete.html'
    success_url = reverse_lazy('dashboard')
