# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Category, Repository


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'created', 'modified', 'slug')
    list_filter = ('owner', 'created', 'modified')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'name',
        'created',
        'modified',
        'category',
        'password',
    )
    list_filter = ('owner', 'created', 'modified', 'category')
    search_fields = ('name',)
