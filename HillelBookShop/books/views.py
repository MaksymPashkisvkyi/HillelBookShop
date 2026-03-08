from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView

from .models import BookModel, CategoryModel, AuthorModel


# Create your views here.
def home(request):
    selected_categories = [v.strip() for v in request.GET.getlist('category') if v.strip()]
    selected_authors = [v.strip() for v in request.GET.getlist('author') if v.strip()]
    selected_sort = request.GET.get("sort", "").strip()

    books_qs = (
        BookModel.objects
        .select_related("category")
        .prefetch_related("authors")
    )

    if selected_categories:
        books_qs = books_qs.filter(category__slug__in=selected_categories)

    if selected_authors:
        books_qs = books_qs.filter(authors__slug__in=selected_authors)

    sort_map = {
        "price_asc": "price",
        "price_desc": "-price",
    }

    books_qs = books_qs.order_by(sort_map.get(selected_sort, "title")).distinct()

    context = {
        "books": books_qs,
        "categories": CategoryModel.objects.all().order_by("name"),
        "authors": AuthorModel.objects.all().order_by("first_name", "last_name"),
        "selected_categories": selected_categories,
        "selected_authors": selected_authors,
        "selected_sort": selected_sort,
    }
    return render(request, 'books/index.html', context=context)


class BookDetailView(DetailView):
    model = BookModel
    context_object_name = "book"
    template_name = "books/page-detail.html"


class AboutView(TemplateView):
    template_name = "about.html"
