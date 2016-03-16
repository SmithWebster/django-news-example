# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.

class NewsItem(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(
            max_length=45,
            blank=False,
            null=False,
            verbose_name="Заголовок",
            help_text="Заголовок задает тему новости"
        )
    content = models.TextField(
            blank=False,
            null=False,
            verbose_name=u"Контент",
            help_text=u"Контент может содержать html-теги для форматирования"
        )
    author = models.ForeignKey('Author', verbose_name="Автор")

    created_at = models.DateTimeField(
            null=False,
            blank=False,
            auto_now_add=True,
            editable=False, verbose_name="Создано"
        )

    class Meta:
        db_table = u'main_news'
        verbose_name = (u'Новость')
        verbose_name_plural = (u'Новости')

    def __unicode__(self):
        return self.title

    def getComments(self):
        comments = News_Comment.objects.filter(news=self).order_by('-created_at').all()
        return comments

class News_Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey('Author', verbose_name="Автор")
    news = models.ForeignKey('NewsItem', verbose_name="Новость")
    comment = models.CharField(max_length=500, blank=False, null=False, verbose_name=u"Комментарий")
    created_at = models.DateTimeField(
            null=False,
            blank=False,
            auto_now_add=True,
            editable=False, verbose_name="Создано"
        )

    class Meta:
        db_table = u'main_news_comments'
        verbose_name = (u'Комментарий')
        verbose_name_plural = (u'Комментарии')

    def __unicode__(self):
        return str(self.author).decode('utf8') + " (" + self.comment[:50] + "...)"

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(
            max_length=20,
            blank=False,
            null=False,
            verbose_name="Имя",
            help_text="Полное имя автора"
        )
    last_name = models.CharField(
            max_length=20,
            blank=False,
            null=False,
            verbose_name="Фамилия",
            help_text="Фамилия автора"
        )
    surename = models.CharField(
            max_length=20,
            blank=True,
            null=True,
            verbose_name="Отчество",
            help_text="Отчество автора (не обязательно)"
        )
    email = models.CharField(
            max_length=45,
            blank=True,
            null=True,
            verbose_name="Эл. почта",
            help_text="Электронная почта автора (для обратной связи; не обязательно)"
        )
    site = models.CharField(
            max_length=45,
            blank=True,
            null=True,
            verbose_name="Сайт",
            help_text="Сайт автора (не обязательно)"
        )

    class Meta:
        db_table = u'main_authors'
        verbose_name = (u'Автор')
        verbose_name_plural = (u'Авторы')

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def register_author(self, response):
        # light registration process
        if not self.id:
            return False
        response.set_cookie('authorId', self.id)
        return True

    @classmethod
    def identify_author(cls, request):
        author = None
        authorId = None
        if 'authorId' in request.COOKIES:
            authorId = int(request.COOKIES.get('authorId'))

        try:
            author = Author.objects.get(pk=authorId)
        except Author.DoesNotExist:
            pass

        return author

