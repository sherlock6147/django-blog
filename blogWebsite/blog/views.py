from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# Create your views here.
from .forms import UserSignupForm,UserLoginForm
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
    print(request.user)
    return render(request,'blog/index.html',context)

def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post':post,
    }
    return render(request,'blog/detail.html',context)

def create(request):
    if(request.method=='POST'):
        time = timezone.now()
        date = request.POST['pub_date'].split('-')
        publishing_time = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),time.hour,time.minute,time.second)
        newPost = Post(post_title=request.POST['post_title'], post_author=request.POST['post_author'],post_text= request.POST['post_text'],pub_date= publishing_time)
        print(newPost.pub_date)
        newPost.save()
    return render(request,'blog/create.html')

def signup(request):
    if (request.method == 'POST'):
        form = UserSignupForm(request.POST)
        print(request.user)
        if form.is_valid():
            try:
                user = form.save()
                username = form.cleaned_data.get('username')
                print(user)
                messages.success(request,'Account was created for '+username)
                return HttpResponseRedirect('/blog/')
            except:
                return HttpResponse("404 an error occured")         
        else:
            form = UserSignupForm()
            context = {
            'form': form,
            }
            return render(request, 'blog/signup.html', context)
    else:
        print(request.user)
        form = UserSignupForm()
        context = {
            'form': form,
        }
        print('GET')
        print(context)
        return render(request, 'blog/signup.html', context)

def loginPage(request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            print("hello")
            login(request, user=user)
            return HttpResponseRedirect('/blog/')
        else:
            messages.info(request,"Incorrect username or password")
            form = UserLoginForm()
            context = {
                'form': form,
            }
            return render(request, 'blog/login.html', context)
    else:
        form = UserLoginForm()
        context = {
            'form': form,
        }
        return render(request, 'blog/login.html', context)

def logoutUser(request):
    username = str(request.user)
    logout(request)
    messages.info(request,"Logged out "+username)
    return HttpResponseRedirect('/blog/login/')