from django.views.generic import TemplateView


class AccountView(TemplateView):
    template_name = 'accounts/pages/page-account.html'
