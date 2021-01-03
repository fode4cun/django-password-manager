from django.urls import path

from pwdgen import views

app_name = 'pwdgen'

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/edit/<slug:slug>/', views.CategoryEditView.as_view(), name='category-edit'),
    path('categories/delete/<slug:slug>/', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('password/save/', views.PasswordCreateView.as_view(), name='password-save'),
    path('categories/<slug:category_slug>/password/delete/<slug:pwd_slug>/', views.PasswordDeleteView.as_view(), name='password-delete'),
    path('search-icon/', views.search_icon, name='search-icon'),
]
