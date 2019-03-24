from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from hyperion.models import Server, Post, Comment
from hyperion.serializers import *

# pylint: disable=invalid-name
# python manage.py test -v=2 hyperion.tests.tests_serializers
class SerializerTestCase(TestCase):

    def setUp(self):
        u = User.objects.create_user(username="foreignserver")
        s1 = Server.objects.create(author=u)

        # user one (foreign user)
        self.u1 = User.objects.create(
            username='2haotianzhu',
            first_name='haotian',
            last_name='zhu',
        )
        self.u1.profile.display_name = "haotian"
        self.u1.profile.host = s1
        self.u1.profile.url = "http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471"

        # user two (local user)
        self.u2 = User.objects.create(
            username='6zhi',
            first_name='zhi',
            last_name='li'
        )
        self.u2.profile.display_name = "zhili"
        self.u2.profile.url = self.u2.profile.get_full_id()

    def test_remote_user_serializer(self):
        serializer = UserSerializer(instance=self.u1)
        data = serializer.data
        self.assertEqual(data['id'], self.u1.profile.get_full_id())
        self.assertEqual(data['first_name'], self.u1.first_name)
        self.assertEqual(data['last_name'], self.u1.last_name)
        self.assertEqual(data['display_name'], self.u1.profile.display_name)
        self.assertEqual(data['url'], self.u1.profile.url)

    def test_local_user_serializer(self):
        serializer = UserSerializer(instance=self.u2)
        data = serializer.data
        self.assertEqual(data['id'], self.u2.profile.get_full_id())
        self.assertEqual(data['first_name'], self.u2.first_name)
        self.assertEqual(data['last_name'], self.u2.last_name)
        self.assertEqual(data['display_name'], self.u2.profile.display_name)
        self.assertEqual(data['url'], self.u2.profile.url)

    def test_comment_serializer(self):
        p1 = Post.objects.create(
            author=self.u1.profile,
            title="u1 post",
            content="test content")

        c1 = Comment.objects.create(
            author=self.u1.profile,
            comment="u1 comment",
            post=p1)

        serializer = CommentSerializer(instance=c1)
        data = serializer.data
        self.assertEqual(data['author']['id'], self.u1.profile.get_full_id())
        self.assertEqual(data['author']['first_name'], self.u1.first_name)
        self.assertEqual(data['author']['last_name'], self.u1.last_name)
        self.assertEqual(data['author']['display_name'], self.u1.profile.display_name)
        self.assertEqual(data['id'], c1.id)
        self.assertEqual(data['content_type'], c1.content_type)
        self.assertEqual(data['comment'], c1.comment)
        self.assertEqual(data['published'], c1.published.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    def test_post_serializer(self):
        post = Post.objects.create(
            author=self.u1.profile,
            title="u1_fof",
            content="test3"
        )
        Comment.objects.create(
            author=self.u1.profile,
            comment="u1 comment",
            post=post
        )
  
        serializer = PostSerializer(post)
        data = serializer.data
        self.assertEqual(data['comments'][0]['comment'], 'u1 comment')
    
    def test_userprofile_username(self):
        serializer = UserProfileSerializer(self.u2.profile)
        self.assertEqual(serializer.data['username'],'6zhi')
