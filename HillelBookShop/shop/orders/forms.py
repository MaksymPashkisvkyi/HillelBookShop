from django import forms
from django.utils.translation import gettext_lazy as _
from shop.orders.models import Order


class OrderCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': _('First name')})
        self.fields['last_name'].widget.attrs.update({'placeholder': _('Last name')})
        self.fields['phone'].widget.attrs.update({'placeholder': _('Phone number')})
        self.fields['email'].widget.attrs.update({'placeholder': _('Email')})

    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': _('City, street, building')}),
        }
