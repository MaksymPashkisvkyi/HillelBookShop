from django.db import models


class CategoryModel(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, verbose_name='Назва категорії')
    slug = models.SlugField(unique=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class BookModel(models.Model):
    title = models.CharField(max_length=100, null=False, verbose_name='Назва книги')
    author = models.CharField(max_length=100, null=False, verbose_name='Автор')
    price = models.DecimalField(decimal_places=2, null=False, max_digits=10, verbose_name='Ціна')
    description = models.TextField(null=False, verbose_name='Опис')
    stock = models.PositiveIntegerField(null=False, default=0, verbose_name='Кількість')
    category_id = models.ForeignKey(CategoryModel, on_delete=models.PROTECT,
                                 verbose_name='Категорія')

    def __str__(self):
        return f'{self.title}. Автор: {self.author}. Кількість: {self.stock}'

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
