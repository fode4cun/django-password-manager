from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'layout/base.html'
