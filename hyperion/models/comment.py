

from datetime import datetime
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from .user import User


class Comment(models.Model):
    '''
    author: User
    create_date: date
    post: Post
    '''
    class Meta:
        app_label = 'hyperion'

    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    content = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(
        'Post',
        related_name='comments',
        on_delete=models.CASCADE
    )
