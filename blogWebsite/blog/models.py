from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    post_title = models.CharField(max_length=100)
    post_author = models.CharField(max_length=60)
    post_text = models.CharField(max_length=2000)
    pub_date = models.DateTimeField('date published')
    post_image = models.ImageField('image',upload_to='images/',null=True,blank=True)
    likes = models.PositiveIntegerField("Number Of Likes",default=0)
    dislikes = models.PositiveIntegerField("Number Of Dislikes",default=0)
    def __str__(self):
        return self.post_title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment_user = models.CharField(max_length=150)
    comment_text = models.CharField(max_length=350)
    def __str__(self):
        return self.comment_text

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    liked_by_user = models.CharField(max_length=150)
    def __str__(self):
        return 'By '+ self.liked_by_user +' On Post '+self.post.post_title

class Dislike(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    disliked_by_user = models.CharField(max_length=150)
    def __str__(self):
        return 'By '+ self.disliked_by_user+' On Post '+self.post.post_title

class ProfilePhoto(models.Model):
    username = models.CharField("username",max_length=150,default="AnonymousUser")
    profile_image = models.ImageField('image',upload_to='user_images/',null=True,blank=True)
    def __str__(self):
        return 'By '+ self.username