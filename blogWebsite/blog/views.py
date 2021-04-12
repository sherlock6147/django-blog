from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
# Create your views here.
from .models import Post
from django.utils import timezone
import datetime
from django.core.paginator import Paginator

def index(request):
    all_posts = Post.objects.order_by('-pub_date').filter(pub_date__lte=timezone.now())
    paginatorObject = Paginator(all_posts, 5)
    pageNumber = request.GET.get('page')
    try:
        pageObj = paginatorObject.get_page(pageNumber)
    except PageNotAnInteger:
        pageObj = paginatorObject.get_page(1)
    except EmptyPage:
        pageObj = paginatorObject.get_page(paginatorObject.num_pages)
    context = {
        'page_obj': pageObj,
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
        time = timezone.now()
        date = request.POST['pub_date'].split('-')
        publishing_time = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),time.hour,time.minute,time.second)
        newPost = Post(post_title=request.POST['post_title'], post_author=request.POST['post_author'],post_text= request.POST['post_text'],pub_date= publishing_time)
        # Post.objects.create(request.POST['post_title'], request.POST['post_author'], request.POST['post_text'], request.POST['pub_date'])
        # time = datetime.date()
        # newPost.pub_date.hour = 4
        # newPost.pub_date.minute = 24
        # newPost.pub_date.second = 32
        print(newPost.pub_date)
        newPost.save()
    return render(request,'blog/create.html')