from django.urls import path

from pwdgen import views

app_name = 'pwdgen'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('password/save/', views.PasswordCreateView.as_view(), name='password-save'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/edit/<slug:slug>/', views.CategoryEditView.as_view(), name='category-edit'),
    path('categories/delete/<slug:slug>/', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('search-icon/', views.search_icon, name='search-icon'),
]
