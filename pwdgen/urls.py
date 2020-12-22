from django.urls import path

from pwdgen.views import HomeView

app_name = 'pwdgen'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
