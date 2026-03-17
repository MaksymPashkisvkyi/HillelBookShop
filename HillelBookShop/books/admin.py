from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Book, Genre, Author

admin.site.unregister(Group)


class BookInline(admin.TabularInline):
    model = Book
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'old_price', 'stock', 'created_at', 'updated_at')
    list_display_links = ('title',)
    list_filter = ('genre', 'author')
    search_fields = ('title', 'author')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    inlines = [BookInline]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
