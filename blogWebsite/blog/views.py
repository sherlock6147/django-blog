from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
# Create your views here.
from .models import Post

def index(request):
    all_posts = Post.objects.order_by('pub_date')
    context = {
        'all_posts':all_posts,
    }
    return render(request,'blog/index.html',context)

def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post':post,
    }
    return render(request,'blog/detail.html',context)

def create(request):
    return render(request,'blog/create.html')