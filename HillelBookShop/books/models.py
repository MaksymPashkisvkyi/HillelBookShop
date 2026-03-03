from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class CategoryModel(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, verbose_name='Назва категорії')
    slug = models.SlugField(unique=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class AuthorModel(models.Model):
    first_name = models.CharField(max_length=100, null=False, verbose_name='Ім\'я')
    last_name = models.CharField(max_length=100, null=False, verbose_name='Прізвище')
    slug = models.SlugField(unique=True, null=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Автори'
        ordering = ['first_name', 'last_name']


class BookModel(models.Model):
    title = models.CharField(max_length=100, null=False, verbose_name='Назва книги')
    slug = models.SlugField(unique=True, null=False)
    ISBN = models.CharField(max_length=17, null=False, verbose_name='ISBN')
    authors = models.ManyToManyField(AuthorModel, related_name="books", verbose_name='Автори')
    price = models.DecimalField(decimal_places=2, null=False, max_digits=10, verbose_name='Ціна',
                                validators=[MinValueValidator(0.0)])
    old_price = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=10, verbose_name='Стара ціна')
    description = models.TextField(null=False, verbose_name='Опис')
    stock = models.PositiveIntegerField(null=False, default=0, verbose_name='Кількість')
    image_url = models.URLField(null=False, default='https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
                                verbose_name='Зображення')
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT,
                                 verbose_name='Категорія')

    def __str__(self):
        return f'{self.title}. Кількість: {self.stock}'

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['title', 'price']
