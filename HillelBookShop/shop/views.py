from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .filters import ProductFilter
from .models import Product


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'shop/catalog/pages/page-home.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('HX-Request') == 'true':
            return render(self.request, 'shop/catalog/partials/product-list.html', context)
        return super().render_to_response(context, **response_kwargs)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/catalog/pages/page-detail.html'
