from django.contrib import messages
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import Http404, HttpResponseServerError
from django.shortcuts import render
from django.template import loader
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView

from layout.forms import UserRegistrationForm
from pwdgen.forms import GeneratorForm, PasswordForm
from pwdgen.generator import Generator


def response_error_400(request, exception=None):
    return render(request, 'layout/page-400.html', status=400)


def bad_request(request):
    raise SuspiciousOperation


def response_error_403(request, exception=None):
    return render(request, 'layout/page-403.html', status=403)


def permission_denied(request):
    raise PermissionDenied


def response_error_404(request, exception=None):
    return render(request, 'layout/page-404.html', status=404)


def page_not_found(request):
    raise Http404


def response_error_500(request):
    return render(request, 'layout/page-500.html', status=500)


def server_error(request):
    template = loader.get_template('layout/page-500.html')
    return HttpResponseServerError(template.render())


@sensitive_post_parameters()
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            messages.success(request, 'The account has created successfully')
        else:
            messages.error(request, 'Error creating your account')
    else:
        user_form = UserRegistrationForm()

    return render(request, 'registration/signup.html', {'user_form': user_form})


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
        context['pwdform'] = PasswordForm(owner=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = GeneratorForm(request.POST)

        if form.is_valid():
            form = GeneratorForm(form.cleaned_data)

        context['form'] = form
        return self.render_to_response(context)


class AccountManage(TemplateView):
    template_name = 'layout/account.html'
