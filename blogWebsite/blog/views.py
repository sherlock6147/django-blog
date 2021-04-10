from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
# Create your views here.
from .models import Post
from django.utils import timezone

def index(request):
    all_posts = Post.objects.order_by('-pub_date').filter(pub_date__lte=timezone.now())
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
    if(request.method=='POST'):
        print(request.POST)
        # newPost = Post.objects.update_or_create(request.POST['post_title'],request.POST['post_author'],request.POST['post_text'],request.POST['pub_date'])
        newPost = Post(post_title=request.POST['post_title'], post_author=request.POST['post_author'],post_text= request.POST['post_text'],pub_date= request.POST['pub_date'])
        # Post.objects.create(request.POST['post_title'], request.POST['post_author'], request.POST['post_text'], request.POST['pub_date'])
        newPost.save()
    return render(request,'blog/create.html')