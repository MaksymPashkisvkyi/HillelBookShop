from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView

from .forms import RegistrationForm, LoginForm, ProfileForm


class ProfileView(LoginRequiredMixin, UpdateView):
    """Display and update the currently authenticated user profile."""

    template_name = 'accounts/pages/page-profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        """Return the currently authenticated user object."""
        return self.request.user


class AccountLoginView(LoginView):
    """Authenticate a user with the custom email-based login form."""

    template_name = 'accounts/pages/page-login.html'
    form_class = LoginForm
    redirect_authenticated_user = True


class RegisterView(CreateView):
    """Register a new user account and redirect to the login page."""

    template_name = 'accounts/pages/form-register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
