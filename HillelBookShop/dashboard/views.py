from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from catalog.models import Book


class DashboardView(ListView):
    queryset = Book.objects.all()
    template_name = 'dashboard/pages/page-dashboard.html'
    context_object_name = 'books'


class BookCreateView(CreateView):
    model = Book
    template_name = 'dashboard/pages/book-create.html'
    fields = '__all__'
    success_url = reverse_lazy('dashboard')


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'dashboard/pages/book-update.html'
    fields = '__all__'
    success_url = reverse_lazy('dashboard')


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'dashboard/pages/book-delete.html'
    success_url = reverse_lazy('dashboard')
