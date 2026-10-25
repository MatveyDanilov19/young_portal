from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import NewsPost, NewsLike, NewsComment
from .forms import NewsCommentForm
from django.core.paginator import Paginator


def news_list(request):
    # Получаем фильтр из GET-параметра (?scope=all, ?scope=main, ?scope=mc)
    scope = request.GET.get('scope', 'all')
    
    if scope == 'main':
        posts = NewsPost.objects.filter(portal_scope='main').order_by('-created_at')
    elif scope == 'mc':
        posts = NewsPost.objects.filter(portal_scope='mc').order_by('-created_at')
    else:
        posts = NewsPost.objects.all().order_by('-created_at')

    # Пагинатор: берем первые 10 для старта, дальше будем подгружать через JS
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj.object_list,
        'has_more': page_obj.has_next(),
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'current_scope': scope,
    }
    return render(request, 'news/news_list.html', context)


def news_detail(request, pk):
    post = get_object_or_404(NewsPost, pk=pk)
    likes_count = post.likes.count()
    comments = post.comments.filter(is_active=True, parent__isnull=True)
    
    user_liked = False
    if request.user.is_authenticated:
        # Это делается в Python, а не в шаблоне — поэтому всё работает
        user_liked = NewsLike.objects.filter(user=request.user, post=post).exists()

    if request.method == 'POST':
        form = NewsCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('news:news_detail', pk=post.pk)
    else:
        form = NewsCommentForm()

    return render(request, 'news/news_detail.html', {
        'post': post,
        'likes_count': likes_count,
        'user_liked': user_liked,          # <-- передаём флаг в шаблон
        'comments': comments,
        'form': form
    })

@login_required
def toggle_like(request, pk):
    post = get_object_or_404(NewsPost, pk=pk)
    like, created = NewsLike.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # Если лайк уже был - удаляем (дизлайк/снять лайк)
    return redirect('news:news_detail', pk=post.pk)

@login_required
def add_comment(request, pk):
    post = get_object_or_404(NewsPost, pk=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            NewsComment.objects.create(
                post=post,
                author=request.user,   # вместо user
                content=text            # вместо text
            )
    return redirect('news:news_detail', pk=post.pk)

@login_required
def news_create(request):
    from .forms import NewsPostForm
    if request.method == 'POST':
        form = NewsPostForm(request.POST, request.FILES)  # <-- важно: request.FILES
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.is_published = True
            post.save()
            return redirect('news:news_detail', pk=post.pk)
    else:
        form = NewsPostForm()
    return render(request, 'news/news_form.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(NewsPost, pk=pk)
    # Проверка: удалять может только автор
    if post.author == request.user:
        post.delete()
    return redirect('news:news_list')
