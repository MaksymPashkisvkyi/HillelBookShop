from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from shop.models import Product, Customer


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', _('Очікує')
        PAID = 'paid', _('Оплачено')
        CREATED = 'created', _('Створено')
        DELIVERED = 'delivered', _('Доставлено')
        CANCELLED = 'cancelled', _('Скасовано')

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_('Користувач'),
    )

    first_name = models.CharField(_('Ім\'я'), max_length=100)
    last_name = models.CharField(_('Прізвище'), max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(_('Телефон'), max_length=13)
    address = models.TextField(_('Адреса'))
    created_at = models.DateTimeField(_('Створено'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Оновлено'), auto_now=True)

    status = models.CharField(
        _('Статус'),
        max_length=30,
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED
    )
    total_price = models.DecimalField(_('Загальна вартість'), max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Замовлення')
        verbose_name_plural = _('Замовлення')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('Замовлення'))
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_('Продукт'))
    price = models.DecimalField(_('Ціна'), max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(_('Кількість'), default=1)

    def get_total(self):
        return Decimal(self.price) * Decimal(self.quantity)

    class Meta:
        verbose_name = _('Одиниця замовлення')
        verbose_name_plural = _('Одиниця замовлення')
