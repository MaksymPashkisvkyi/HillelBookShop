from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from payments.models import Payment
from shop.models import Product, Customer


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PAID = 'paid', _('Paid')
        CREATED = 'created', _('Created')
        DELIVERED = 'delivered', _('Delivered')
        CANCELLED = 'cancelled', _('Cancelled')

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_('User'),
    )

    first_name = models.CharField(_('First name'), max_length=100)
    last_name = models.CharField(_('Last name'), max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(_('Phone'), max_length=13)
    address = models.TextField(_('Address'))
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    status = models.CharField(
        _('Status'),
        max_length=30,
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED
    )
    total_price = models.DecimalField(_('Total price'), max_digits=12, decimal_places=2)
    payment = models.OneToOneField(
        Payment,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.email}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('Order'))
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_('Product'))
    price = models.DecimalField(_('Price'), max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)

    def get_total(self):
        return Decimal(self.price) * Decimal(self.quantity)

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')
