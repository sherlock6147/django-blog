from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import math
# Create your views here.
from .forms import UserSignupForm,UserLoginForm,AddComment,AddProfilePhotoForm
from django.forms import ImageField
from .models import Post,Comment,Like,ProfilePhoto
from django.utils import timezone
import datetime
from django.core.paginator import Paginator

def index(request):
    all_posts = Post.objects.order_by('-pub_date').filter(pub_date__lte=timezone.now())
    postPerPage = 5
    postCount = all_posts.count()
    last_page = math.ceil(postCount/postPerPage) 
    paginatorObject = Paginator(all_posts, postPerPage)
    pageNumber = request.GET.get('page')
    try:
        pageObj = paginatorObject.get_page(pageNumber)
    except PageNotAnInteger:
        pageObj = paginatorObject.get_page(1)
    except EmptyPage:
        pageObj = paginatorObject.get_page(paginatorObject.num_pages)
    context = {
        'page_obj': pageObj,
        'last_page' : last_page,
        'before_last_page' : last_page-1,
    }
    print(request.user)
    return render(request,'blog/index.html',context)

def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    all_comments = Comment.objects.filter(post=post)
    all_likes = Like.objects.filter(post=post)
    if (request.method == 'POST'):
        if 'comment' in request.POST:
            form = AddComment(request.POST)
            if form.is_valid():
                comment = Comment()
                comment.post = post
                comment.comment_user = request.user.username
                comment.comment_text = request.POST.get('comment_text')
                print(comment.comment_user)
                comment.save()
            else:
                form = AddComment()
                context = {
                    'post': post,
                    'form': form,
                    'all_comments' : all_comments,
                }
                print("else 1")
                return render(request,'blog/detail.html',context)
        elif 'like' in request.POST:
            form = AddComment()
            like = Like.objects.filter(post=post,liked_by_user=request.user.username)
            # print(like.count())
            if(like.count()==0):
                newLike = Like()
                newLike.post = post
                newLike.liked_by_user = request.user.username
                print('liked')
                newLike.save()
                post.likes = post.likes + 1
                post.save()
            else:
                print('already liked')
        elif 'dislike' in request.POST:
            form = AddComment()
            try:
                like = Like.objects.filter(post=post,liked_by_user=request.user.username)
                print('disliked')
                like.delete()
                post.likes = post.likes - 1
                post.save()
            except:
                print("like not found for deleteion")
        else:
            form = AddComment()
    else:
        form = AddComment()
    context = {
        'post': post,
        'form': form,
        'all_comments' : all_comments,
        'numberOfLikes' : all_likes.count(),
    }
    return render(request,'blog/detail.html',context)

def create(request):
    if(request.method=='POST'):
        time = timezone.now()
        date = request.POST['pub_date'].split('-')
        publishing_time = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),time.hour,time.minute,time.second)
        newPost = Post(post_title=request.POST['post_title'], post_author=request.user.username,post_text= request.POST['post_text'],pub_date= publishing_time)
        print(newPost.pub_date)
        if(request.FILES['post_image'] is not None):
            newPost.post_image = request.FILES['post_image']
        newPost.save()
        return HttpResponseRedirect('/blog/'+str(newPost.id))
    return render(request,'blog/create.html')

def signup(request):
    if (request.method == 'POST'):
        form = UserSignupForm(request.POST)
        print(request.user)
        if form.is_valid():
            print('form is valid')
            try:
                # User Created Successfully
                user = form.save()
                username = form.cleaned_data.get('username')
                print(user)
                messages.success(request,'Account was created for '+username)
                login(request, user=user)
                return HttpResponseRedirect('/blog/')
            except:
                form = UserSignupForm()
                context = {
                'form': form,
                }
                return render(request, 'blog/signup.html', context)       
        else:
            # Invalid Form
            print('form is invalid')
            # form = UserSignupForm()
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

def profile(request):
    has_profile_photo=False
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        user_obj=user
        print(ProfilePhoto.objects.filter(username=user.username).count())
        form = AddProfilePhotoForm()
        if ProfilePhoto.objects.filter(username=user.username).count()<1:
            print("loop 1")
            if request.method=='POST':
                print("loop 2")
                form = AddProfilePhotoForm(request.POST,request.FILES)
                print(request.FILES)
                if form.is_valid():
                    inst = form.save(commit=False)
                    print("loop 6")
                    inst.username = user.username
                    inst.save()
                    has_profile_photo=True
                else:
                    print("loop 7")
                    form = AddProfilePhotoForm()
                profile_photo=ProfilePhoto.objects.filter(username=user.username).first()
                print(profile_photo)
            else:
                form = AddProfilePhotoForm()
                print("loop 3")
                profile_photo=None
        else:
            print("loop 4")
            profile_photo=ProfilePhoto.objects.filter(username=user.username).first()
            has_profile_photo=True
        users_post = Post.objects.order_by('-pub_date').filter(post_author=user.username)
    else:
        print("loop 5")
        user_obj='AnonymousUser'
        users_post = None
    context = {
        'user_obj' : user_obj,
        'has_profile_photo': has_profile_photo,
        'profile_photo': profile_photo,
        'form':form,
        'users_posts':users_post,
    }    
    return render(request,template_name='blog/profile.html',context=context)

def editPost(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    if request.method == 'POST':
        time = timezone.now()
        date = request.POST['pub_date'].split('-')
        publishing_time = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),time.hour,time.minute,time.second)
        newPost = Post(post_title=request.POST['post_title'], post_author=request.user.username,post_text= request.POST['post_text'],pub_date= publishing_time)
        print(newPost.pub_date)
        if(request.POST['post_image'] is not None):
            newPost.post_image = request.POST['post_image']
        post = newPost
        post.save()
        return HttpResponseRedirect('/blog/'+str(post_id))
    context = {'post':post,}
    return render(request,'blog/edit.html',context)

def deletePost(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    if request.method == 'POST' and request.user.username == post.post_author:
        if 'confirm' in request.POST:
            # delete post
            post.delete()
            return HttpResponseRedirect('/blog/')
        if 'cancel' in request.POST:
            #redirect to post
            return HttpResponseRedirect('/blog/'+str(post_id))
    context = {'post':post,}
    return render(request,'blog/delete.html',context)