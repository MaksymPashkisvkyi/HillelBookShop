import django_filters
from django import forms

from .models import Category, Author, Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category',
        label='category',
        queryset=Category.objects.all(),
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
        model = Product
        fields = ['name', 'category', 'author', 'price_min', 'price_max']
