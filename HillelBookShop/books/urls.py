# store/urls.py
from django.urls import path
from .views import BookDetailView, AboutView, BookListView

urlpatterns = [
    path('', BookListView.as_view(), name='home'),
    path('detail/<slug:slug>/', BookDetailView.as_view(), name='book_detail'),
    path('about/', AboutView.as_view(), name='about'),
]
