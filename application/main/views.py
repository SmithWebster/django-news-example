# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template import Template, RequestContext
from django.shortcuts import render_to_response

from application.main.models import *

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponse

from application.main.forms import NewsCommentForm
from application.main.forms import NewsAddForm

# Create your views here.

def render_view(request, template, params):
    return render_to_response(template, params, context_instance=RequestContext(request))

def home(request):
    c = {}
    return render_view(request, "home.html", c)

def news_list(request):
    c = {}

    news = NewsItem.objects.order_by('-created_at').all()

    paginator = Paginator(news, 10)

    page = request.GET.get('page')

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    c.update({
        'news': news,
        'paginator': paginator,
    })

    return render_view(request, "news-list.html", c)

def news_add(request):
    response = redirect(reverse(u'news-add'))

    form = None
    if request.method == "POST":
        form = NewsAddForm(request.POST)

        if form.is_valid():
            news = NewsItem()

            author = Author.identify_author(request)
            if not author:
                try:
                    author = Author.objects.filter(
                        first_name=form.cleaned_data.get('first_name'),
                        last_name=form.cleaned_data.get('last_name')
                    ).get()
                except Author.DoesNotExist:
                    author = Author.objects.create(
                        first_name=form.cleaned_data.get('first_name'),
                        last_name=form.cleaned_data.get('last_name'),
                        surename=form.cleaned_data.get('surename'),
                        email=form.cleaned_data.get('email'),
                        site=form.cleaned_data.get('site')
                    )
                author.register_author(response)

            news.title = form.cleaned_data.get("title")
            news.content = form.cleaned_data.get("content")
            news.author = author
            news.save()

            messages.success(request, 'Новость опубликована')
            return response
        else:
            if form.errors:
                raise Exception(form.errors)
                for field in form:
                    messages.error(request, field.errors)

    c = {}
    c.update({
        'author': Author.identify_author(request),
    })
    return render_view(request, "news-add.html", c)

def news_view(request, news_id):
    c = {}
    newsItem = None

    try:
        newsItem = NewsItem.objects.get(pk=news_id)
    except NewsItem.DoesNotExist:
        pass

    c.update({
        'newsItem': newsItem,
        'author': Author.identify_author(request),
    })

    return render_view(request, "news-view.html", c)

def comment_post(request, news_id):
    news_id = int(news_id)
    response = redirect(reverse(u'news-view', args=(news_id,)))

    newsItem = None
    try:
        newsItem = NewsItem.objects.get(pk=news_id)
    except NewsItem.DoesNotExist:
        return redirect(reverse(u'news-view', args=(news_id,)))

    comment = None
    form = None
    if request.method == "POST":

        form = NewsCommentForm(request.POST)

        if form.is_valid():
            comment = News_Comment()

            author = Author.identify_author(request)
            if not author:
                try:
                    author = Author.objects.filter(
                        first_name=form.cleaned_data.get('first_name'),
                        last_name=form.cleaned_data.get('last_name')
                    ).get()
                except Author.DoesNotExist:
                    author = Author.objects.create(
                        first_name=form.cleaned_data.get('first_name'),
                        last_name=form.cleaned_data.get('last_name'),
                        surename=form.cleaned_data.get('surename'),
                        email=form.cleaned_data.get('email'),
                        site=form.cleaned_data.get('site')
                    )
                author.register_author(response)

            comment.comment = form.cleaned_data.get("comment")
            comment.news = newsItem
            comment.author = author
            comment.save()

            messages.success(request, 'Комментарий опубликован')
        else:
            if form.errors:
                raise Exception(form.errors)
                for field in form:
                    messages.error(request, field.errors)

    return response

