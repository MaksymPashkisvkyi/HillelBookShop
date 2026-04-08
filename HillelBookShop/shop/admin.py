from django.contrib import admin

from .models import Category, Author, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'price', 'discount_price', 'stock', 'created_at', 'updated_at')
    list_display_links = ('name',)
    list_filter = ('category', 'author')
    search_fields = ('name', 'author')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    inlines = [ProductInline]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
