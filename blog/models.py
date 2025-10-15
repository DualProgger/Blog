from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

"""
Создание модели постов моего блога
"""
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    # поле даты публикации
    publish = models.DateTimeField(default=timezone.now)
    # поле даты создания
    created = models.DateTimeField(auto_now_add=True)
    # поле даты изменения
    updated = models.DateTimeField(auto_now=True)
    # создаем поле для выбора записи: черновик(DF) или опубликовать(PB)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    
    class Meta:
        # способ сортировки по-умолчанию(по убыванию даты публикации)
        ordering = ['-publish']
        # индексация записей в БД для ускорения поиска записей
        indexes = [
            models.Index(fields=['-publish']),
        ]
    
    # строковое представление объекта Post - это будет его заголовок
    def __str__(self):
        return self.title
