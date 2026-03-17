from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView, ListView
from .filters import BookFilter

from .models import Book, Genre


class BookListView(ListView):
    queryset = Book.objects.all()
    template_name = 'books/pages/page-home.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = BookFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('HX-Request') == 'true':
            return render(self.request, 'books/partials/product-list.html', context)
        return super().render_to_response(context, **response_kwargs)


class BookDetailView(DetailView):
    model = Book
    context_object_name = "book"
    template_name = "books/pages/page-detail.html"


class AboutView(TemplateView):
    template_name = "about.html"
