from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

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

class CategoryCreateUpdateMixin:
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("pwdgen:category-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CategoryCreateView(CategoryCreateUpdateMixin, CreateView):
    pass


class CategoryEditView(CategoryCreateUpdateMixin, UpdateView):
    def get_initial(self):
        initial = super().get_initial()
        initial.update({'url': 'Image already exists'})
        return initial


class CategoryDeleteView(TemplateView):
    template_name = 'pwdgen/confirm.html'

    def post(self, request, slug):
        category = get_object_or_404(Category, slug=slug, owner=request.user)
        category.delete()
        return redirect(reverse_lazy("pwdgen:category-list"))

@require_GET
def search_icon(request):
    param = request.GET.get('word')
    results = get_icons(param)
    return JsonResponse({'results': results})
