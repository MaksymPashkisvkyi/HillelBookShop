from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Category(MPTTModel):
    name = models.CharField(_('Name'), max_length=200)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name=_('Parent category'))
    is_active = models.BooleanField(_('Active'), default=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Author(models.Model):
    name = models.CharField(_('Full name'), max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        ordering = ['name']


class ActiveProductManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_active=True, stock__gt=0)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='products')

    name = models.CharField(_('Name'), max_length=300)
    slug = models.SlugField(unique=True, null=False)
    description = models.TextField(_('Description'))
    ISBN = models.CharField(max_length=17, null=False)
    price = models.DecimalField(_('Price'), max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(_('Discount'), max_digits=12, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(_('Quantity'), default=0)
    image = models.ImageField(_('Image'), upload_to='product_images/')
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)
    is_active = models.BooleanField(_('Active'), default=True)

    objects = models.Manager()
    active = ActiveProductManager()

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(check=Q(stock__gte=0), name='non_negative_stock'),
            models.CheckConstraint(check=Q(price__gte=0), name='non_negative_price'),
        ]

    def __str__(self):
        return _('%(name)s. Price: %(price)s') % {
            'name': self.name,
            'price': self.current_price,
        }

    @property
    def current_price(self):
        return self.discount_price or self.price


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    address = models.CharField(_('Address'), max_length=200, blank=True)

    def __str__(self) -> str:
        return self.user.get_full_name() or self.user.email

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
