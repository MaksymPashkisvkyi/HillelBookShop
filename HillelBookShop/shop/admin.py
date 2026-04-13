from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category, Author, Product, Customer
from .orders.models import Order, OrderItem


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_author_name', 'price', 'discount_price', 'stock', 'created_at', 'updated_at')
    list_display_links = ('name',)
    list_filter = ('category', 'author')
    search_fields = ('name', 'author')
    list_editable = ('price', 'discount_price', 'stock')

    @admin.display(description=_('Автор'))
    def get_author_name(self, obj):
        return f'{obj.author.name}'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active')
    inlines = [ProductInline]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'created_at', 'updated_at')
    list_editable = ('status',)
    list_filter = ('status',)
    search_fields = ('customer',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'quantity')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'address')
    list_display_links = ('user',)
