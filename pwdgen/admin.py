# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Category, Password


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'created',
        'modified',
        'owner',
        'slug',
        'image',
    )
    list_filter = ('created', 'modified', 'owner')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'created',
        'modified',
        'category',
        'password',
    )
    list_filter = ('created', 'modified', 'category')
    search_fields = ('name',)
