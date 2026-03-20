from django.urls import path
from .views import DashboardView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('book-create/', BookCreateView.as_view(), name='book_create'),
    path('book-update/<slug:slug>/', BookUpdateView.as_view(), name='book_update'),
    path('book-delete/<slug:slug>/', BookDeleteView.as_view(), name='book_delete'),
]
