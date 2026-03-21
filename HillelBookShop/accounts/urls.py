from cProfile import Profile

from django.urls import path
from .views import ProfileView, RegisterView
from .forms import UserLoginForm
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(
        template_name="accounts/pages/page-login.html",
        authentication_form=UserLoginForm,
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
