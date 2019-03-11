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
        #friend of hyuntian
        self.u_1 = User.objects.create_user(
            username='2haotianzhu',
            first_name='haotian',
            last_name='zhu',
            password='123456')
        # friend of 2haotianzhu
        self.u_2 = User.objects.create_user(
            username='hyuntian',
            first_name='yuntian',
            last_name='zhang',
            password='123456')
        Friend.objects.create(profile1=self.u_1.profile, profile2=self.u_2.profile)
        # foaf 2haotianzhu friend of hyuntian
        self.u_3 = User.objects.create_user(
            username='yuntian1',
            first_name='yuntian',
            last_name='zhang',
            password='123456')
        Friend.objects.create(profile1=self.u_2.profile, profile2=self.u_3.profile)
        # foaf 2haotianzhu friend of hyuntian
        self.u_4 = User.objects.create_user(
            username='yuntian2',
            first_name='yuntian',
            last_name='zhang',
            password='123456')
        Friend.objects.create(profile1=self.u_2.profile, profile2=self.u_4.profile)
        # public stranger
        self.u_5 = User.objects.create_user(
            username='stranger',
            first_name='yuntian',
            last_name='zhang',
            password='123456')
        # private stranger
        self.u_6 = User.objects.create_user(
            username='_stranger',
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

        #own
        p_5 = Post.objects.create(author=self.u_1.profile, title="5", content="test",visibility ="PRIVATE")
        p_5 .visible_to.set([self.u_1.profile])
        
        #public
        Post.objects.create(
            author=self.u_5.profile, title="6", content="test",visibility ="PUBLIC")
        #friends
        Post.objects.create(
            author=self.u_2.profile, title="7", content="test",visibility ="FRIENDS")
        #foaf
        Post.objects.create(
            author=self.u_4.profile, title="8", content="test",visibility ="FOAF")
   
        #private can see
        p_10 = Post.objects.create(author=self.u_6.profile, title="10", content="test",visibility ="PRIVATE")
        p_10.visible_to.set([self.u_1.profile])
            
        #private cant see
        Post.objects.create(
            author=self.u_5.profile, title="9", content="test",visibility ="PRIVATE")
        response = self.client.get('/author/posts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['query'], 'posts')
        self.assertEqual(len(response.data['posts']), 5)

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
