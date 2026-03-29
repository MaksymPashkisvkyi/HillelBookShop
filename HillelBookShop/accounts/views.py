from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView

from .forms import RegistrationForm, LoginForm


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/pages/page-profile.html'


class AccountLoginView(LoginView):
    template_name = 'accounts/pages/page-login.html'
    form_class = LoginForm
    redirect_authenticated_user = True


class RegisterView(CreateView):
    template_name = 'accounts/pages/form-register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
