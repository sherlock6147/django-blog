from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
# Create your views here.
from .models import Blog

def index(request):
    all_blogs = Blog.objects.order_by('pub_date')
    context = {
        'all_blogs':all_blogs,
    }
    return render(request,'blog/index.html',context)

def detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    context = {
        'blog':blog,
    }
    return render(request,'blog/detail.html',context)
