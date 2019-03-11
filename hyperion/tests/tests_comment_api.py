import base64
from rest_framework.test import APITestCase
from hyperion.models import *
from hyperion.serializers import PostSerializer, UserProfileSerializer
from hyperion.views import post_views
from django.test import TestCase, Client
from django.conf import settings

# python manage.py test -v=2 hyperion.tests.tests_comment_api

class CommentViewTestCase(TestCase):
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

        self.u_1.profile.display_name = "Yuntian"
        self.u_1.profile.url = "http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471"
        self.u_1.profile.github = "http://github.com/Yuntian"
        self.p_1 = Post.objects.create(
            title="A post title",
            author=self.u_1.profile,
            content_type="text/plain",
            content="some post content",
            visibility="PUBLIC",
            unlisted="False")

        credentials = base64.b64encode('{}:{}'.format(
            self.username, self.password).encode()).decode()
        self.client = Client(HTTP_AUTHORIZATION='Basic {}'.format(credentials))

    def test_auth_post_a_post(self):
        data = {
            "query": "createComment",
            "post":"http://hyperion.com/posts/1",
            "comment":{
                "author":{
                    "host": "http://127.0.0.1:5454/",
                    "display_name": "Yuntian",
                    "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                    "github": "http://github.com/Yuntian"
                },
                "comment":"heyya",
                "content_type":"text/markdown",
            }
        }

        response = self.client.post('posts/1/comments', data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['query'], 'createComment')
        self.assertEqual(response.data['success'], True)
        self.assertEqual(Comment.objects.all()[0].author.display_name, '2haotianzhu')
        self.assertEqual(Comment.objects.all()[0].comment, 'heyya')