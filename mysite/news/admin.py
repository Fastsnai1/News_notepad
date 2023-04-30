from django.contrib import admin

from .models import *


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'photo', 'is_published')  # то что видино на дисплее
    list_display_links = ('id', 'title')  # поля на которые можно кликнуть и перейти на соответствующию статью
    search_fields = ('title', 'content')  # поля по которым можно отсортировать
    list_editable = ('is_published',)  # список редактируемых полей
    list_filter = ("is_published", 'created_at')  # список полей по которым можэно будет фильтровать
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
