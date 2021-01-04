from django.urls import path, include, re_path
from allauth.account import views
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from allauth.socialaccount.providers.google.provider import GoogleProvider

urlpatterns_socials = default_urlpatterns(GoogleProvider)

urlpatterns = [
    path('signup/', views.signup, name='account_signup'),
    path('login/', views.login, name='account_login'),
    path('logout/', views.logout, name='account_logout'),
    # Email
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        views.confirm_email,
        name="account_confirm_email",
    ),
    path('', include(urlpatterns_socials)),
]