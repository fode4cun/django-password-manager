from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from pwdgen.forms import CategoryForm, PasswordForm
from pwdgen.models import Category, Password
from pwdgen.utils import decrypt_password, get_icons


class CategoryCreateUpdateMixin(LoginRequiredMixin):
    model = Category
    form_class = CategoryForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CategoryCreateView(CategoryCreateUpdateMixin, CreateView):
    pass


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = super().get_object()
        pwd_qs = category.categories.all()

        for pwd in pwd_qs:
            pwd.password = decrypt_password(pwd.password)

        context['pwd_qs'] = pwd_qs
        return context


class CategoryEditView(CategoryCreateUpdateMixin, UpdateView):
    def get_initial(self):
        initial = super().get_initial()
        initial.update({'url': 'Image already exists'})
        return initial


class CategoryDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'pwdgen/confirm.html'

    def post(self, request, slug):
        category = get_object_or_404(Category, slug=slug, owner=request.user)
        category.delete()
        return redirect(reverse_lazy("pwdgen:category-list"))


class PasswordCreateView(LoginRequiredMixin, CreateView):
    model = Password
    form_class = PasswordForm

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'POST':
            return super().dispatch(*args, **kwargs)

        return HttpResponseForbidden('Forbidden 403')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)


class PasswordDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'pwdgen/confirm.html'

    def post(self, request, category_slug, pwd_slug):
        category = get_object_or_404(Category, slug=category_slug, owner=request.user)
        password = get_object_or_404(Password, category=category, slug=pwd_slug)
        password.delete()
        return redirect(reverse_lazy("pwdgen:category-detail", args=[category_slug]))


@login_required
@require_GET
def search_icon(request):
    param = request.GET.get('word')
    results = get_icons(param)
    return JsonResponse({'results': results})
