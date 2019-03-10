from rest_framework.test import APITestCase
from hyperion.models import *
from hyperion.serializers import PostSerializer, UserProfileSerializer
from hyperion.views import post_views
from django.test import TestCase, Client
from django.conf import settings

# python manage.py test -v=2 hyperion.tests.tests_post_api


class CommentViewTestCase(TestCase):
    def setUp(self):
        
    def test_auth_post_a_post(self):
            data = {
                "query": "createPost",
                "post": {
                    "title": "test",
                    "content_type": "text/plain",
                    "content": "some post content",
                }
            }
            response = self.client.post(
                '/author/posts', data, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['query'], 'createPost')
            self.assertEqual(response.data['success'], True)
            self.assertEqual(Post.objects.all()[0].author.display_name,
                            '2haotianzhu')