from django.db import models
from django.contrib.auth.models import User


class Server(models.Model):
    """
    This class is to save foreign server information
    """

    # the author's username and password are used for receiving other server's request
    author = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="server", null=True, blank=True
    )
    # API endpoint of the server
    url = models.CharField(max_length=200, blank=True)
    endpoint = models.CharField(max_length=200, blank=True)
    # this username and password are used for sending request to other server
    foreign_db_username = models.TextField(null=True, blank=True)
    foreign_db_password = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "hyperion"
