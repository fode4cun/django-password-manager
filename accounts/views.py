from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import CreateView

from accounts.forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'
    redirect_authenticated_user = True

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.success_url
            if redirect_to == self.request.path:
                raise ValueError(
                        "Redirection loop for authenticated user detected. Check that "
                        "your LOGIN_REDIRECT_URL doesn't point to a login page."
                        )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)
