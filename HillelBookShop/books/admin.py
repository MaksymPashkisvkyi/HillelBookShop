from django.contrib import admin
from django.contrib.auth.models import Group

from .models import BookModel, CategoryModel, AuthorModel

admin.site.unregister(Group)


class BookInline(admin.TabularInline):
    model = BookModel
    extra = 1


@admin.register(BookModel)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_authors', 'price', 'old_price', 'stock')
    list_display_links = ('title',)
    list_filter = ('category', 'authors')
    search_fields = ('title', 'authors__first_name', 'authors__last_name')

    def get_authors(self, obj):
        return ", ".join(str(author) for author in obj.authors.all())

    get_authors.short_description = 'Authors'


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    inlines = [BookInline]


@admin.register(AuthorModel)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'slug')

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    full_name.short_description = 'Ім\'я та прізвище'
