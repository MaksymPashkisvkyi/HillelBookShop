from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from .models import UserProfile


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput())
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput())

    class Meta:
        model = UserProfile
        fields = ['email', 'phone', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': _('Type here'), 'autocomplete': 'given-name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': _('Type here'), 'autocomplete': 'family-name'})
        self.fields['email'].widget.attrs.update({'placeholder': _('Enter email address'), 'autocomplete': 'email'})
        self.fields['phone'].widget.attrs.update({'placeholder': _('Phone number'), 'autocomplete': 'tel'})
        self.fields['password1'].widget.attrs.update({'placeholder': _('Enter password'), 'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'placeholder': _('Repeat password'), 'autocomplete': 'new-password'})

    def clean(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Email'), widget=forms.EmailInput())
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': _('Enter email')})
        self.fields['password'].widget.attrs.update({'placeholder': _('Enter your password')})


class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'class': 'form-control', 'type': 'date'}
        )
    )

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter first name')}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter last name')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Enter email')}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter phone number')}),
        }
