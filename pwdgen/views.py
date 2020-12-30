from django.http.response import JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView

from pwdgen.forms import CategoryForm, GeneratorForm
from pwdgen.generator import Generator
from pwdgen.models import Category
from pwdgen.utils import get_icons


class HomeView(TemplateView):
    template_name = 'pwdgen/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {
            'length_range': '12',
            'lowercase': ['on'],
            'uppercase': ['on'],
            'punctuation': ['on'],
            'numbers': ['on'],
        }

        password = Generator(data).gen()
        data.update({'password': password})

        context['form'] = GeneratorForm(initial=data)

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = GeneratorForm(request.POST)

        if form.is_valid():
            form = GeneratorForm(form.cleaned_data)

        context['form'] = form
        return self.render_to_response(context)


class CategoryListView(ListView):
    model = Category


class CategoryFormView(FormView):
    form_class = CategoryForm
    template_name = 'pwdgen/category_form.html'

    def get_success_url(self):
        return reverse("pwdgen:category-list")

    def form_valid(self, form):
        category = form.save(self.request)
        return super().form_valid(form)


@require_GET
def search_icon(request):
    param = request.GET.get('word')
    results = get_icons(param)
    return JsonResponse({'results': results})
