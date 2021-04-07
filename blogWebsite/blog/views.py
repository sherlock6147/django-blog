from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
# Create your views here.
from .models import Blog

def index(request):
    all_blogs = Blog.objects.order_by('pub_date')
    html = ""
    for blog in all_blogs:
        html = html + blog.blog_title + '<br>'
    print(html)
    return HttpResponse(html)

def detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    print(blog)
    return HttpResponse("This is the detail of the blog : %s" % blog.blog_text)
