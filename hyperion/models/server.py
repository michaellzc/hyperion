from django.db import models
from django.core.exceptions import ValidationError


class Server(models.Model):
    '''
    '''

    name = models.CharField(max_length=200)
    accept = models.BooleanField(default=True)
    class Meta:
        app_label = 'hyperion'
        unique_together = ('name',)
