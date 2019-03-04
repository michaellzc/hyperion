import base64
from rest_framework.test import APITestCase
from hyperion.models import *
from hyperion.serializers import PostSerializer, UserProfileSerializer
from hyperion.views import post_views
from django.test import TestCase, Client
from django.conf import settings

# python manage.py test -v=2 hyperion.tests.tests_post_api


class PostViewTestCase(TestCase):
    username = '2haotianzhu'
    password = '123456'

    def setUp(self):
        self.u_1 = User.objects.create_user(
            username='2haotianzhu',
            first_name='haotian',
            last_name='zhu',
            password='123456')
        self.u_2 = User.objects.create_user(
            username='hyuntian',
            first_name='yuntian',
            last_name='zhang',
            password='123456')
        credentials = base64.b64encode('{}:{}'.format(
            self.username, self.password).encode()).decode()
        self.client = Client(HTTP_AUTHORIZATION='Basic {}'.format(credentials))

    def test_get_one(self):
        Post.objects.create(
            author=self.u_1.profile, title="1", content="test1")
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['posts']), 1)
        self.assertEqual(response.data['posts'][0]['author']['display_name'],
                         '2haotianzhu')

    def test_get_many(self):
        Post.objects.create(
            author=self.u_1.profile, title="2", content="test2")
        Post.objects.create(
            author=self.u_1.profile, title="3", content="test3")
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['posts']), 2)

    def test_get_post_by_id(self):
        Post.objects.create(
            author=self.u_1.profile, title="4", content="test4")
        the_id = Post.objects.get().pk
        path = '/posts/{}'.format(the_id)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['post']['author']['display_name'],
                         '2haotianzhu')

    def test_get_auth_posts(self):
        # get post by auth
        Post.objects.create(
            author=self.u_1.profile, title="5", content="test5")
        Post.objects.create(
            author=self.u_2.profile, title="6", content="test6")
        response = self.client.get('/author/posts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['query'], 'posts')
        self.assertEqual(len(response.data['posts']), 1)

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
