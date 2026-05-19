from django.views.generic import TemplateView


class AboutView(TemplateView):
    """Render the static about page."""

    template_name = "pages/about.html"
