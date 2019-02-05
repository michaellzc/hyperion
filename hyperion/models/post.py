
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    '''
    author: User
    create_date: date
    last_modify_date: date
    comments: [Comment]
    '''
    class Meta:
        app_label = 'hyperion'
    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    last_modify_date = models.DateTimeField(default=timezone.now)
