from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post


# вывод на страницу всех ОПУБЛИКОВАННЫХ постов
def post_list(request):
    # создаем объект класса Paginator с постраничной разбивкой
    #  на 3 поста на каждой странице для всех 
    # ОПУБЛИКОВАННЫХ постов all_posts 
    all_posts = Post.published.all()
    paginator = Paginator(all_posts, 3)
    # метод, который пытается получить значение параметра page 
    # из словаря request.GET. Если параметр page не найден, 
    # то метод вернет значение по умолчанию – 1 (то есть, 
    # это будет первая страница)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
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