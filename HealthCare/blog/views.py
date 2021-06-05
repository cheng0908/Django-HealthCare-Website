from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Post, Categories, Likes
from .forms import PostForm, CommentForm
from blog import models
from taggit.models import Tag
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.contrib import auth


@login_required(login_url='login/post_homepage')
def home_view(request):
    user = request.user
    categories = Categories.objects.all()
    posts = Post.objects.all().order_by('-published', ).filter(enabled=True)
    post_author = Post(author=user)
    common_tags = Post.tags.most_common()[:4]
    form = PostForm(request.POST, request.FILES, instance=post_author)
    post_form = PostForm()
    if form.is_valid():
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        newpost.save()
        form.save_m2m()

    return render(request, 'blog/home.html', locals())


@login_required(login_url='login/post_homepage')
def detail_view(request, slug):
    user = request.user
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            # return redirect('detail_view', slug=post.slug)
            return HttpResponseRedirect('/blog/post/{}/'.format(post.slug))
    else:
        form = CommentForm()

    context = {
        'post': post,
        'form': form,
        'user': user,
    }
    return render(request, 'blog/detail.html', context)


@login_required(login_url='login/post_homepage')
def tagged(request, slug):
    user = request.user
    tag = get_object_or_404(Tag, slug=slug)
    common_tags = Post.tags.most_common()[:4]
    posts = Post.objects.filter(enabled=True).filter(tags=tag)
    context = {
        'tag': tag,
        'common_tags': common_tags,
        'posts': posts,
        'user': user,
    }

    return render(request, 'blog/home.html', context)


def homepage(request):
    posts = Post.objects.all().filter(category='3').filter(enabled=True).order_by('-published', )
    common_tags = Tag.objects.all()
    form_c = CommentForm()

    try:
        post_slug = request.POST['slug']
        comment_name = request.POST['name']
        comment_email = request.POST['email']
        comment_body = request.POST['body']
    except:
        post_slug = None

    if request.method == 'POST' and post_slug is not None:
        post = models.Post.objects.get(slug=post_slug)
        comment_post = models.Comment.objects.create(post=post, name=comment_name, body=comment_body, email=comment_email)
        comment_post.save()

    return render(request, 'blog/nutrition.html', locals())


def blog_sport(request):
    posts = Post.objects.all().filter(category='1').filter(enabled=True).order_by('-published', )
    common_tags = Tag.objects.all()
    form_c = CommentForm()

    try:
        post_slug = request.POST['slug']
        comment_name = request.POST['name']
        comment_email = request.POST['email']
        comment_body = request.POST['body']
    except:
        post_slug = None

    if request.method == 'POST' and post_slug is not None:
        post = models.Post.objects.get(slug=post_slug)
        comment_post = models.Comment.objects.create(post=post, name=comment_name, body=comment_body, email=comment_email)
        comment_post.save()

    return render(request, 'blog/sport.html', locals())


def blog_weight_lost(request):
    posts = Post.objects.all().filter(category='2').filter(enabled=True).order_by('-published', )
    common_tags = Tag.objects.all()
    form_c = CommentForm()

    try:
        post_slug = request.POST['slug']
        comment_name = request.POST['name']
        comment_email = request.POST['email']
        comment_body = request.POST['body']
    except:
        post_slug = None

    if request.method == 'POST' and post_slug is not None:
        post = models.Post.objects.get(slug=post_slug)
        comment_post = models.Comment.objects.create(post=post, name=comment_name, body=comment_body, email=comment_email)
        comment_post.save()

    return render(request, 'blog/weight_lost.html', locals())


@login_required(login_url='login/blog_homepage')
def like(request, slug):
    user = request.user
    post = get_object_or_404(Post, slug=slug)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        like = Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1

    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()

    return redirect('blog_homepage')


def test(request):
    categories = Categories.objects.all()
    posts = Post.objects.all().order_by('-published', )
    common_tags = Post.tags.most_common()[:4]
    form = PostForm(request.POST, request.FILES)
    post_form = PostForm()
    if form.is_valid():
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        newpost.save()
        form.save_m2m()
    # else:
    #     c_t = request.POST['title']
    #     c_d = request.POST['description']
    #     c_c = request.POST['content']
    #     c_t = request.POST['tags']

    context = {
        'posts': posts,
        'common_tags': common_tags,
        'form': form,
    }

    return render(request, 'blog/Blog_test.html', locals())
