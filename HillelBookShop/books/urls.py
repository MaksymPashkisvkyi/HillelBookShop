# store/urls.py
from django.urls import path
from .views import home, about, BookDetailView

urlpatterns = [
    path('', home, name='home'),
    path('product/<slug:slug>/', BookDetailView.as_view(), name='detail'),
    path('about/', about, name='about'),

]
