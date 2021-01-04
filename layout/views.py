from django.shortcuts import render
from django.views.generic import TemplateView

from pwdgen.forms import GeneratorForm, PasswordForm
from pwdgen.generator import Generator


def forbidden_403(request, exception):
    return render(request, 'layout/page-403.html', status=403)


def page_not_found_404(request, exception):
    return render(request, 'layout/page-404.html', status=404)


def server_error_500(request):
    return render(request, 'layout/page-500.html', status=500)


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
        data.update({'pwd': password})

        context['form'] = GeneratorForm(initial=data)
        context['pwdform'] = PasswordForm()

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = GeneratorForm(request.POST)

        if form.is_valid():
            form = GeneratorForm(form.cleaned_data)

        context['form'] = form
        return self.render_to_response(context)
