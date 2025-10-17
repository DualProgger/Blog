from django.shortcuts import render, get_object_or_404
from .models import Post


# вывод на страницу всех ОПУБЛИКОВАННЫХ постов
def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})

# Вывод информации о конкретном посте
def post_detail(request, id):
    """
    данная строка заменяет блок try/except;
    id=id, status=Post.Status.PUBLISHED - это именованные аргументы,
    по которым происходит фильтрация
    """
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request, 'blog/post/detail.html', {'post': post})