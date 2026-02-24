from django.contrib import admin
from .models import BookModel, CategoryModel

admin.site.register(BookModel)
admin.site.register(CategoryModel)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category')
