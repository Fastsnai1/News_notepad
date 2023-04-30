"""Тут находяться миксины, для избежания повторения кода"""
from django.db.models import Count

from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 1  # число постов на странице

    def get_user_context(self, **kwargs):
        context = kwargs
        # cats = Category.objects.all()
        cats = Category.objects.annotate(Count('news')) # теперь коллекция иммет свойство (количество постов)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            """проверяем афтаризован ли пользователь"""
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
