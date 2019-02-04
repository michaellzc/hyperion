
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .post import Post



class Comment(models.Model):
    '''
    author: User
    create_date: date
    post: Post
    id: UUID
    '''
    class Meta:
        app_label = 'hyperion'

    COMMENT_CONTENT_TYPE_CHOICE = (
        ('text/plain', 'text/plain'),
        ('text/markdown', 'text/markdown')
    )

    content_type = models.CharField(
        max_length=20,
        choices=COMMENT_CONTENT_TYPE_CHOICE,
        default='text/plain')
    comment = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    def __str__(self):
        return self.comment
