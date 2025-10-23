from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from .models import Post


class PostListView(ListView):
    """
    Альтернативное представление списка постов
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

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

# Обработка данных переданных из формы
def post_share(request, post_id):
    # Извлечь пост по идентификатору id
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            # ... отправить электронное письмо
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form})