from django.db import models
import datetime
from django.utils import timezone
# Create your models here.
class Post(models.Model):
    post_title = models.CharField(max_length=100)
    post_author = models.CharField(max_length=60)
    post_text = models.CharField(max_length=400)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.post_title