from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from .forms import RegistrationForm


class ProfileView(TemplateView):
    template_name = 'accounts/pages/page-profile.html'


class RegisterView(CreateView):
    template_name = 'accounts/pages/form-register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
