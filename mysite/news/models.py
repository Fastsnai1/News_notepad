from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name="Контент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время публикации")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name="Фото")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name="Категории")

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # ссылка на данный класс
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категории')
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):  # ссылка на данный класс
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'
        ordering = ['id']
