# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.

from application.main.models import *

class AuthorAdmin(admin.ModelAdmin):
    search_fields = (
        'first_name',
        'last_name',
        'surename',
        'email',
        'site',
    )
    list_display = (
        'first_name',
        'last_name',
        'surename',
        'email',
        'site',
    )

class NewsItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = (
        'title',
        'content',
        'author',
        'created_at',
    )
    list_display = (
        'title',
        'content',
        'author',
        'created_at',
    )
    list_filter = (
        'created_at',
    )

class News_CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = (
        'news',
        'comment',
        'author',
        'created_at',
    )
    list_display = (
        'news',
        'comment',
        'author',
        'created_at',
    )
    list_filter = (
        'created_at',
    )

admin.site.register(Author, AuthorAdmin)
admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(News_Comment, News_CommentAdmin)
