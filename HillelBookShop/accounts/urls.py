from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import ProfileView, RegisterView, AccountLoginView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
