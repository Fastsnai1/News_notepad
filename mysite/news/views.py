from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
        ]


def index(request):
    posts = News.objects.all()
    cats = Category.objects.all()
    context = {'posts': posts,
               'menu': menu,
               'cats': cats,
               'title': 'big web',
               'cat_selected': 0,
               }
    return render(request, 'news/index.html', context=context)


def about(request):
    return render(request, 'news/about.html', {'menu': menu, 'title': 'low web'})


def addpage(request):
    return HttpResponse('1')


def contact(request):
    return HttpResponse('2')


def login(request):
    return HttpResponse('3')


def show_post(request, post_id):
    return HttpResponse(f'sdadasd{post_id}')


def show_category(request, cat_id):
    posts = News.objects.filter(cat_id=cat_id)
    cats = Category.objects.all()

    # if len(posts) == 0:
    #     raise Http404()

    context = {'posts': posts,
               'menu': menu,
               'cats': cats,
               'title': 'Отображение про категориям',
               'cat_selected': cat_id,
               }
    return render(request, 'news/index.html', context=context)
