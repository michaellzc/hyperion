
from datetime import datetime
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from hyperion.models import Server
from django.test import TestCase
from django.core.exceptions import ValidationError


# python manage.py test -v=2 hyperion.models.tests_server

class ServerTestCase(TestCase):
    def setup(self):
        pass

    def test_create_server(self):
        s1 = Server.objects.create(name='hhahaha')
        self.assertEquals(Server.objects.get().name, 'hhahaha')