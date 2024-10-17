from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from .forms import EmailPostForms, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count


def post_share(request, post_id):
    # Pobieranie posta wedlug identyfikatora.
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Formularz został przesłany.
        form = EmailPostForms(request.POST)
        if form.is_valid():
            # Pomyślnie zweryfikowano poprawność pól formularza.
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} zaleca Ci przeczytanie {post.title}"
            message = f"Przeczytaj {post.title} pod adresem {post_url}\n\n komentarze {cd['name']}: {cd['comments']}"
            send_mail(subject, message, 'lukasz-waclawek@wp.pl', [cd['to']])
            sent = True
    else:
        form = EmailPostForms()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,slug=post,
                             publish__year=year, publish__month=month, publish__day=day
                             )
    # Lista aktywnych komentarzy do tego posta
    comments = post.comments.filter(active=True)
    # Formularz do wprowadzania komentarzy użytkowników
    form = CommentForm()

    # Lista podobnych postów
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
        
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts})


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Stronicowanie z 3 postami na stronę.
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Jeśli zmienna page_number nie jest liczbą całkowitą zwraca pierwszą stronę.
        posts = paginator.page(1)
    except EmptyPage:
        # Jeśli zmienna page_number jest poza zakresem zwraca ostatnią stronę wyników.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # Opublikowano komentarz
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Utwórz obiekt Comment bez zapisywania go w bazie danych
        comment = form.save(commit=False)
        # Przypisz post do komentarza
        comment.post = post
        # Zapisz komentarz do bazy danych
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'body'),).filter(search=query)
    
    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})
