from django.urls import path
from .views import BookDetailView, BookListView

urlpatterns = [
    path('', BookListView.as_view(), name='catalog'),
    path('catalog/', BookListView.as_view(), name='catalog'),
    path('book-detail/<slug:slug>/', BookDetailView.as_view(), name='book_detail')
]
