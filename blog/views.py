from django.shortcuts import render, get_object_or_404
from .models import Post


# вывод на страницу всех ОПУБЛИКОВАННЫХ постов
def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})

# Вывод информации о конкретном посте
def post_detail(request, year, month, day, slug):
    """
    данная строка заменяет блок try/except;
    year, month, day, slug, status=Post.Status.PUBLISHED -
    это именованные аргументы,
    по которым происходит фильтрация
    """
    post = get_object_or_404(Post, 
                             status=Post.Status.PUBLISHED, 
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug)
    return render(request, 'blog/post/detail.html', {'post': post})