from django.core.validators import MinValueValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, verbose_name='Назва жанру')
    slug = models.SlugField(unique=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанри'


class Author(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True, verbose_name='Ім\'я та прізвище')
    slug = models.SlugField(unique=True, null=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Автори'
        ordering = ['name']


class Book(models.Model):
    title = models.CharField(max_length=100, null=False, verbose_name='Назва книги')
    slug = models.SlugField(unique=True, null=False)
    ISBN = models.CharField(max_length=17, null=False, verbose_name='ISBN')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False, verbose_name='Автор')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=False, verbose_name='Жанр')
    price = models.DecimalField(decimal_places=2, null=False, max_digits=10, verbose_name='Ціна',
                                validators=[MinValueValidator(0.0)])
    old_price = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=10, verbose_name='Стара ціна')
    description = models.TextField(null=False, verbose_name='Опис')
    stock = models.PositiveIntegerField(null=False, default=0, verbose_name='Кількість')
    image = models.ImageField(upload_to='book_images/', null=False, verbose_name='Зображення')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Змінено')

    def __str__(self):
        return f'{self.title}. Кількість: {self.stock}'

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['title', 'price']
