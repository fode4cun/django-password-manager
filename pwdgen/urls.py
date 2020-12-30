from django.urls import path

from pwdgen import views

app_name = 'pwdgen'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', views.CategoryFormView.as_view(), name='category-create'),
    path('search-icon/', views.search_icon, name='search-icon'),
]
