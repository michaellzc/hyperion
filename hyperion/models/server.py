from django.db import models
from django.contrib.auth.models import User


class Server(models.Model):
    '''
    This class is to save foreign server information
    '''
    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='server',
        null=True,
        blank=True)

    class Meta:
        app_label = 'hyperion'
