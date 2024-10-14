from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForms
from django.core.mail import send_mail


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
    
    return render(request, 'blog/post/detail.html', {'post': post})


def post_list(request):
    post_list = Post.published.all()
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

    return render(request, 'blog/post/list.html', {'posts': posts})
