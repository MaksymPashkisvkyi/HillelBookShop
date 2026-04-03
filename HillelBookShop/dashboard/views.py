from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from catalog.models import Book


class DashboardView(LoginRequiredMixin, ListView):
    queryset = Book.objects.all()
    template_name = 'dashboard/pages/page-dashboard.html'
    context_object_name = 'books'


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    permission_required = 'catalog.add_book'
    template_name = 'dashboard/pages/book-create.html'
    fields = '__all__'
    success_url = reverse_lazy('dashboard')


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    permission_required = 'catalog.change_book'
    template_name = 'dashboard/pages/book-update.html'
    fields = '__all__'
    success_url = reverse_lazy('dashboard')


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalog.delete_book'
    template_name = 'dashboard/pages/book-delete.html'
    success_url = reverse_lazy('dashboard')
