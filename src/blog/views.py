from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.db.models import Q
from django.http import HttpResponse
from blog.models import BlogPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account

def create_blog_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    
    form  = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateBlogPostForm()

    context['form'] = form

    return render(request, "blog/create_blog.html", context)


def detail_blog_view(request, slug):
    context = {}
    blog_post = get_object_or_404(BlogPost, slug=slug)
    context['blog_post'] = blog_post

    return render(request, 'blog/detail_blog.html', context)

def edit_blog_view(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")

    blog_post = get_object_or_404(BlogPost, slug=slug)

    if blog_post.author != user:
        return HttpResponse("You're not the author")


    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post )
        if form.is_valid():
            obj = form.save(comit=False)
            obj.save()
            context['succes_message'] = "Updated your work"
            blog_post = obj
            
    form = UpdateBlogPostForm(
            initial={
                "title" : blog_post.title,
                "body" : blog_post.body,
                "image" : blog_post.image,
            }
        )
    context['form'] = form
    return render(request, 'blog/edit_blog.html', context)


def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        post = BlogPost.objects.filter(
            Q(title_icontains=q) |
            Q(bofy_icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)
    
    return list(set(queryset))