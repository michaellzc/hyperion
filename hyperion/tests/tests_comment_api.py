import base64
from rest_framework.test import APITestCase
from hyperion.models import *
from hyperion.serializers import PostSerializer, UserProfileSerializer
from hyperion.views import post_views
from django.test import TestCase, Client
from django.conf import settings

# python manage.py test -v=2 hyperion.tests.tests_comment_api


class CommentViewTestCase(TestCase):
    username_1 = "2haotianzhu"
    password_1 = "123456"

    username_2 = "hyuntian"
    password_2 = "123456"

    username_3 = "yuntian1"
    password_3 = "123456"

    server_username = "test_server"
    server_password = "test_server_password"
    server_host = "https://cmput404-front.herokuapp.co"
    home_host = settings.HYPERION_HOSTNAME

    def setUp(self):
        # friend of hyuntian
        self.u_1 = User.objects.create_user(
            username="2haotianzhu", first_name="haotian", last_name="zhu", password="123456"
        )

        self.s_1 = User.objects.create_user(
            username=self.server_username, password=self.server_password
        )
        UserProfile.objects.filter(author=self.s_1).update(url=self.server_host)
        Server.objects.create(author=self.s_1, url=self.server_host)

        # friend of 2haotianzhu
        self.u_2 = User.objects.create_user(
            username="hyuntian", first_name="yuntian", last_name="zhang", password="123456"
        )
        Friend.objects.create(profile1=self.u_1.profile, profile2=self.u_2.profile)

        # foaf 2haotianzhu friend of hyuntian
        self.u_3 = User.objects.create_user(
            username="yuntian1", first_name="yuntian", last_name="zhang", password="123456"
        )
        Friend.objects.create(profile1=self.u_2.profile, profile2=self.u_3.profile)

        # foaf 2haotianzhu friend of hyuntian
        self.u_4 = User.objects.create_user(
            username="yuntian2", first_name="yuntian", last_name="zhang", password="123456"
        )
        Friend.objects.create(profile1=self.u_2.profile, profile2=self.u_4.profile)

        # public stranger
        self.u_5 = User.objects.create_user(
            username="stranger", first_name="yuntian", last_name="zhang", password="123456"
        )

        # private stranger
        self.u_6 = User.objects.create_user(
            username="_stranger", first_name="yuntian", last_name="zhang", password="123456"
        )

        self.p_1 = Post.objects.create(
            title="A post title",
            author=self.u_1.profile,
            content_type="text/plain",
            content="some post content",
            visibility="PRIVATE",
            unlisted="False",
        )

        self.p_1.visible_to.set([self.u_1.profile, self.u_3.profile])

        self.p_2 = Post.objects.create(
            title="A post title",
            author=self.u_1.profile,
            content_type="text/plain",
            content="some post content",
            visibility="PUBLIC",
            unlisted="False",
        )
        self.client = None

        self.s_1 = Server.objects.create()
        self.f_u_1 = UserProfile.objects.create(
            display_name="haotian",
            host=self.s_1,
            url="https://cmput404-front-t2.herokuapp.com/author/1d698d25ff008f7538453c120f581471",
        )

    def test_new_comment(self):
        credentials = base64.b64encode(
            "{}:{}".format(self.username_3, self.password_3).encode()
        ).decode()
        self.client = Client(HTTP_AUTHORIZATION="Basic {}".format(credentials))

        data = {
            "query": "addComment",
            "post": "{}/posts/{}".format(self.home_host, str(self.p_1.id)),
            "comment": {
                "author": {
                    "id": "{}/author/{}".format(self.home_host, str(self.u_3.profile.id)),
                    "host": self.home_host,
                    "display_name": str(self.u_3.profile.display_name),
                },
                "comment": "heyya",
                "content_type": "text/markdown",
            },
        }
        response = self.client.post(
            "/posts/{}/comments".format(str(self.p_1.id)), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "addComment")
        self.assertEqual(response.data["success"], True)
        self.assertEqual(
            Comment.objects.all()[0].author.display_name, self.u_3.profile.display_name
        )
        self.assertEqual(Comment.objects.all()[0].comment, "heyya")

    def test_new_comment_403(self):
        credentials = base64.b64encode(
            "{}:{}".format(self.username_2, self.password_2).encode()
        ).decode()
        self.client = Client(HTTP_AUTHORIZATION="Basic {}".format(credentials))

        data = {
            "query": "addComment",
            "post": "{}/posts/{}".format(self.home_host, str(self.p_1.id)),
            "comment": {
                "author": {
                    "id": "{}/author/{}".format(self.home_host, str(self.u_2.profile.id)),
                    "host": self.home_host,
                    "display_name": str(self.u_2.profile.display_name),
                },
                "comment": "heyya",
                "content_type": "text/markdown",
            },
        }
        response = self.client.post(
            "/posts/{}/comments".format(str(self.p_1.id)), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    def test_comment_foreign(self):
        credentials = base64.b64encode(
            "{}:{}".format(self.server_username, self.server_password).encode()
        ).decode()
        self.client = Client(HTTP_AUTHORIZATION="Basic {}".format(credentials))

        data = {
            "query": "addComment",
            "post": "{}/posts/{}".format(self.home_host, str(self.p_2.id)),
            "comment": {
                "author": {
                    "id": "https://{}/author/{}".format(self.server_host, str(self.f_u_1.id)),
                    "host": self.server_host,
                    "display_name": str(self.f_u_1.display_name),
                },
                "comment": "heyya",
                "content_type": "text/markdown",
            },
        }
        response = self.client.post(
            "/posts/{}/comments".format(str(self.p_2.id)), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
