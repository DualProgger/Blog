from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


"""
Определяем собственный менеджер моделей
"""
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)



"""
Создание модели постов моего блога
"""
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    title = models.CharField(max_length=250)
    # параметр unique_for_date говорит полю slug должно быть 
    # уникальным для каждой даты, сохраненной в поле publish. 
    # Это означает, что два поста могут иметь одинаковый slug, 
    # если они опубликованы в разные дни.
    slug = models.SlugField(max_length=250, unique_for_date='publish')
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
    # менеджер, применяемый по умолчанию
    objects = models.Manager()
    # пользовательский менеджер
    published = PublishedManager()
    # добавляем функционал тэгирования
    tags = TaggableManager()
    
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
    
    # в качестве главного url-адреса берем конкретную запись блога по его id, т.е.
    # По этому имени будет извлечён шаблон URL 'blog/<int:id>/', в который 
    # будет подставлено значение аргумента id. Например, для объекта 
    # с id равным 7, будет получен такой URL: /blog/7/
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'