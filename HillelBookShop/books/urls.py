# store/urls.py
from django.urls import path
from .views import home, BookDetailView, AboutView

urlpatterns = [
    path('', home, name='home'),
    path('product/<slug:slug>/', BookDetailView.as_view(), name='detail'),
    path('about/', AboutView.as_view(), name='about'),
]
