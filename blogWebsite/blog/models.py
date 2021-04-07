from django.db import models
import datetime
from django.utils import timezone
# Create your models here.
class Blog(models.Model):
    blog_title = models.CharField(max_length=100)
    blog_author = models.CharField(max_length=60)
    blog_text = models.CharField(max_length=400)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.blog_title