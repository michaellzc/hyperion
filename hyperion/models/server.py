from django.db import models



class Server(models.Model):
    '''
    This class is to save foreign server information
    '''

    name = models.CharField(max_length=200)
    accept = models.BooleanField(default=True)
    password = models.CharField(max_length=20, null=True)

    class Meta:
        app_label = 'hyperion'
        unique_together = ('name',)
