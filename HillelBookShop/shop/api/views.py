from rest_framework import filters, viewsets
from shop.models import Product, Category
from shop.api.serializers import (
    ProductSerializer,
    CategorySerializer,
    ProductDetailSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Expose active root categories for read-only API consumers."""

    queryset = Category.objects.filter(is_active=True, parent__isnull=True).prefetch_related('children')
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Expose searchable and orderable read-only product API endpoints."""

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name']
    lookup_field = 'slug'

    def get_queryset(self):
        """Return active products filtered by optional price boundaries."""
        qs = Product.active.all().select_related('category', 'author')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)

        return qs

    def get_serializer_class(self):
        """Use a richer serializer for detail views and a compact one for lists."""
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer
