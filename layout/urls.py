from django.urls import path

from layout import views

app_name = 'layout'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('400/', views.bad_request),
    path('403/', views.permission_denied),
    path('404/', views.page_not_found),
    path('500/', views.server_error),
]
