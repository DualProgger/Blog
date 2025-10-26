from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post

register = template.Library()

# выводит общее количество ОПУБЛИКОВАННЫХ постов
@register.simple_tag
def total_posts():
    return Post.published.count()

# Выводит последние 5(по-умолчанию, можно передать значение как аргумент) постов
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

# выводит пост с наибольшим количеством комментариев
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).exclude(total_comments=0).order_by('-total_comments')[:count]

# пользовательский фильтр для html-разметки
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
