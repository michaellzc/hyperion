from django.db import models
from django.core.exceptions import ValidationError


class Server(models.Model):
    '''
    '''
    class Meta:
        app_label = 'hyperion'

    name = models.CharField(max_length=200)
    accept = models.BooleanField(default=True)