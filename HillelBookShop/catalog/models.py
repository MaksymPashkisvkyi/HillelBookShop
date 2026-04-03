from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


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
    discount_price = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=10, verbose_name='Стара ціна')
    description = models.TextField(null=False, verbose_name='Опис')
    stock = models.PositiveIntegerField(null=False, default=0, verbose_name='Кількість')
    image = models.ImageField(upload_to='book_images/', null=False, verbose_name='Зображення')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Змінено')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(check=Q(stock__gt=0), name='non_negative_stock'),
            models.CheckConstraint(check=Q(price__gt=0), name='non_negative_price'),
        ]

    def __str__(self):
        return f'{self.title}. Кількість: {self.price}'

    @property
    def current_price(self):
        return self.discount_price or self.price

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='<UNK>')
    name = models.CharField(max_length=100, null=False, verbose_name='<UNK> <UNK>')