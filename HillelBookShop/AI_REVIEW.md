# AI Review

This file documents AI-assisted review for 3 complex parts of the project. Recommendations were validated manually before applying them.

## 1. `payments.views.PaymentViewSet.confirm`

### Original code

```python
@action(detail=True, methods=['post'])
def confirm(self, request, pk=None):
    payment = self.get_object()
    order_id = request.data.get('order_id')
    if not order_id:
        return Response({
            'error': _('order_id is required'),
        }, status=status.HTTP_400_BAD_REQUEST)

    order = get_object_or_404(Order, id=order_id)
    order.payment = payment
    order.save()
```

### AI recommendations

- Restrict order lookup to the authenticated user to avoid linking another user's order.
- Use `update_fields` for a narrower save.
- Add a clearer responsibility docstring for the custom action.

### Final code

```python
@action(detail=True, methods=['post'])
def confirm(self, request, pk=None):
    """Confirm a payment, link it to an order, and send the receipt email."""
    payment = self.get_object()
    order_id = request.data.get('order_id')
    if not order_id:
        return Response({
            'error': _('order_id is required'),
        }, status=status.HTTP_400_BAD_REQUEST)

    order = get_object_or_404(Order, id=order_id, customer__user=request.user)
    order.payment = payment
    order.save(update_fields=['payment'])
```

### Why accepted

This was a valid security and maintainability improvement. It reduces accidental cross-user order linking and keeps the write operation narrower.

## 2. `shop.orders.views.order_create`

### Original code

```python
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
```

### AI recommendations

- Replace the bare `except:` with a specific exception.
- Use `bulk_create` for order items created from the cart.
- Add a docstring clarifying the flow.

### Final code

```python
def order_create(request):
    """Create an order from the current cart and redirect to checkout."""
    ...
    if request.user.is_authenticated:
        try:
            order.customer = request.user.customer
        except Customer.DoesNotExist:
            customer, created = Customer.objects.get_or_create(user=request.user)
            order.customer = customer
    order.save()

    order_items = []
    for item in cart:
        order_items.append(OrderItem(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['quantity']
        ))
    OrderItem.objects.bulk_create(order_items)
```

### Why accepted

These changes are valid and reduce both risk and query count. The specific exception improves clarity, and `bulk_create` is a good fit because order items are created together in one batch.

## 3. `shop.api.views.ProductViewSet`

### Original code

```python
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name']
    lookup_field = 'slug'

    def get_queryset(self):
        qs = Product.active.all().select_related('category')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        ...
```

### AI recommendations

- Load related author data together with category to reduce future N+1 risks.
- Add docstrings to explain API intent and queryset filtering behavior.
- Prefetch category children in the category API root queryset.

### Final code

```python
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Expose active root categories for read-only API consumers."""
    queryset = Category.objects.filter(is_active=True, parent__isnull=True).prefetch_related('children')
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Expose searchable and orderable read-only product API endpoints."""
    ...

    def get_queryset(self):
        """Return active products filtered by optional price boundaries."""
        qs = Product.active.all().select_related('category', 'author')
        ...
```

### Why accepted

This is a low-risk improvement that makes the API code clearer and slightly more future-proof for related-object access.
