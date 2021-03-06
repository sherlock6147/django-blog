from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('signup/', views.signup, name='signup'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('<int:post_id>/edit',views.editPost,name='editpost'),
    path('<int:post_id>/delete',views.deletePost,name='deletepost'),
]