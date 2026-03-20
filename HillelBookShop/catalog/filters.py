import django_filters
from django import forms

from catalog.models import Book, Genre, Author


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    genre = django_filters.ModelMultipleChoiceFilter(
        field_name='genre',
        label='Genre',
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    author = django_filters.ModelMultipleChoiceFilter(
        field_name='author',
        label='Author',
        queryset=Author.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    price_min = django_filters.NumberFilter(
        field_name='price',
        label='Мінімальна',
        widget=forms.NumberInput(attrs={'placeholder': '$0.01'}),
        lookup_expr='gte'
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        label='Максимальна',
        widget=forms.NumberInput(attrs={'placeholder': '$1000'}),
        lookup_expr='lte'
    )
    sort = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),
        ),
        choices={
            ('title', 'за замовчуванням'),
            ('price', 'за зростанням ціни'),
            ('-price', 'за зменшенням ціни'),
        }
    )

    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'price_min', 'price_max']
