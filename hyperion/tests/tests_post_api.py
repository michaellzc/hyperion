from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from hyperion.models import *
from hyperion.views import post_views
from rest_framework.test import APIClient
from django.test import TestCase
# python manage.py test -v=2 hyperion.tests.tests_post_api


class PostViewTestCase(APITestCase, TestCase):

    def setUp(self):
        self.u_1 = User.objects.create(
            username='2haotianzhu',
            first_name='haotian',
            last_name='zhu'
        )
        self.u_2 = User.objects.create(
            username='hyuntian',
            first_name='yuntian',
            last_name='zhang'
        )
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_get_one(self):
        Post.objects.create(
            author=self.u_1.profile,
            title="1",
            content="test1"
        )
        response = self.client.get('/posts')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author']['display_name'], '2haotianzhu')

    def test_get_many(self):
        Post.objects.create(
            author=self.u_1.profile,
            title="2",
            content="test2"
        )
        Post.objects.create(
            author=self.u_1.profile,
            title="3",
            content="test3"
        )
        response = self.client.get('/posts')
        self.assertEqual(len(response.data), 2)

    def test_get_post_by_id(self):
        Post.objects.create(
            author=self.u_1.profile,
            title="4",
            content="test4"
        )
        the_id = Post.objects.get().pk
        path = '/posts/{}'.format(the_id)
        response = self.client.get(path)
        self.assertEqual(
            response.data['author']['display_name'],
            '2haotianzhu'
        )

    def test_get_auth_posts(self):
        # get post by auth
        Post.objects.create(
            author=self.u_1.profile,
            title="5",
            content="test5"
        )
        Post.objects.create(
            author=self.u_2.profile,
            title="6",
            content="test6"
        )
        request = self.factory.get('/auth/posts')
        request.user = self.u_1
        view = post_views.PostViewSet.as_view({'get': 'get_auth_posts'})
        response = view(request)
        self.assertEqual(len(response.data), 1)

    def test_auth_post_a_post(self):
        data = {
            "title":"6",
            "content":"test6",
        }
        request = self.factory.post('/auth/posts', data)
        request.user = self.u_1
        view = post_views.PostViewSet.as_view({'post': 'post_auth_posts'})
        response = view(request)
        print(response)

