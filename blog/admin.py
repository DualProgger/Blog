from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # отображение соответствующих полей модели Post
    list_display = ['title', 'slug', 'author', 'publish', 'status']

    # фильтрация данных по заданным полям
    list_filter = ['status', 'created', 'publish', 'author']

    # строка поиска по заданным полям
    search_fields = ['title', 'body']

    # автоматические заполнение поля slug на основе поля title
    prepopulated_fields = {'slug': ('title',)}

    # поисковый виджет удобнее вместо выпадающего списка для выбора автора
    raw_id_fields = ['author']

    # Навигационные ссылки, предназначенные для перемещения по иерархии дат
    date_hierarchy = 'publish'

    # сортировка по-умолчанию
    ordering = ['status', 'publish']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
    