from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *
from .utils import *


class NewsHome(DataMixin, ListView):
    model = News
    template_name = 'news/index.html'  # путь к шаблону
    context_object_name = 'posts'
    extra_context = {'title': 'О сайте'}  # этот словарь может принемать только статические данные

    def get_context_data(self, *, object_list=None, **kwargs):
        """передаёт в шаблон как статические так и динамические данные"""
        context = super().get_context_data(**kwargs)  # получаем контекст который уже сформирован для шаблона
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))  # формируем общий словарь контекста

    def get_queryset(self):
        """Эта функция возвращиет данны в model, если нужно с условием"""
        return News.objects.filter(is_published=True)


# def index(request):
#     posts = News.objects.all()
#     context = {'posts': posts,
#                'menu': menu,
#                'title': 'big web',
#                'cat_selected': 0,
#                }
#     return render(request, 'news/index.html', context=context)


def about(request):
    return render(request, 'news/about.html', {'menu': menu, 'title': 'low web'})


# class AddPage(CreateView):
#     form_class = AddPostForm # тип формы длжен быть форма связанная с моделью
#     template_name = 'news/addpage.html'
#     success_url = reverse_lazy('home') # маршрут куда вернуться после добавления формы(get_absolute_url)

#     def get_context_data(self, *, object_list=None, **kwargs):
#         """передаёт в шаблон как статические так и динамические данные"""
#         context = super().get_context_data(**kwargs)  # получаем контекст который уже сформирован для шаблона
#         context['menu'] = menu
#         context['title'] = 'Добавление статьи'
#         return context

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            try:
                News.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, "Ошибка добавления поста!")
    else:
        form = AddPostForm()
    return render(request, 'news/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


def contact(request):
    return HttpResponse('2')


# def login(request):
#     return HttpResponse('3')


class ShowPost(DataMixin, DetailView):
    model = News
    template_name = 'news/post.html'
    slug_url_kwarg = 'post_slug'
    # pk_url_kwarg =
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        """передаёт в шаблон как статические так и динамические данные"""
        context = super().get_context_data(**kwargs)  # получаем контекст который уже сформирован для шаблона
        c_def = self.get_user_context(title='post')
        return dict(list(context.items()) + list(c_def.items()))


# def show_post(request, post_slug):
#     post = get_object_or_404(News, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'news/post.html', context=context)


class NewsCategory(DataMixin, ListView):
    model = News
    template_name = 'news/index.html'  # путь к шаблону
    context_object_name = 'posts'
    allow_empty = False  # если выдаёться ошибка, то перекидывает на страницу 404

    def get_context_data(self, *, object_list=None, **kwargs):
        """передаёт в шаблон как статические так и динамические данные"""
        context = super().get_context_data(**kwargs)  # получаем контекст который уже сформирован для шаблона
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return News.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


class RegisterUser(DataMixin, CreateView):
    """Регистрация пользователя"""
    form_class = RegisterUserForm
    template_name = 'news/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        """передаёт в шаблон как статические так и динамические данные"""
        context = super().get_context_data(**kwargs)  # получаем контекст который уже сформирован для шаблона
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))  # формируем общий словарь контекста

    def form_valid(self, form):
        """если регистрация успешна, то сразу авторизует пользователя"""
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    """Авторизация пользователя"""
    form_class = LoginUserForm
    template_name = 'news/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """передаёт в шаблон как статические так и динамические данные"""
        context = super().get_context_data(**kwargs)  # получаем контекст который уже сформирован для шаблона
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))  # формируем общий словарь контекста

    def get_success_url(self):
        """переадресация при успешной авторизации"""
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')