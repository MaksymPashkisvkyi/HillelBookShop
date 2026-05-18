import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Category, Author, Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category',
        label=_('Category'),
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    author = django_filters.ModelMultipleChoiceFilter(
        field_name='author',
        label=_('Author'),
        queryset=Author.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    price_min = django_filters.NumberFilter(
        field_name='price',
        label=_('Minimum'),
        widget=forms.NumberInput(attrs={'placeholder': _('From')}),
        lookup_expr='gte'
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        label=_('Maximum'),
        widget=forms.NumberInput(attrs={'placeholder': _('To')}),
        lookup_expr='lte'
    )
    sort = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),
        ),
        choices={
            ('title', _('Default')),
            ('price', _('Price: low to high')),
            ('-price', _('Price: high to low')),
        }
    )

    class Meta:
        model = Product
        fields = ['name', 'category', 'author', 'price_min', 'price_max']
