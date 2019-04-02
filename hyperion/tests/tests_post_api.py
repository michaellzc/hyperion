import base64
from rest_framework.test import APITestCase
from hyperion.models import *
from hyperion.serializers import PostSerializer, UserProfileSerializer
from hyperion.views import post_views
from django.test import TestCase, Client
from django.conf import settings
import requests

# python manage.py test -v=2 hyperion.tests.tests_post_api


class PostViewTestCase(TestCase):
    username = "2haotianzhu"
    password = "123456"

    def setUp(self):
        # friend of hyuntian
        self.u_1 = User.objects.create_user(
            username="2haotianzhu", first_name="haotian", last_name="zhu", password="123456"
        )
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

        credentials = base64.b64encode(
            "{}:{}".format(self.username, self.password).encode()
        ).decode()
        self.client = Client(HTTP_AUTHORIZATION="Basic {}".format(credentials))

    def test_get_one(self):
        Post.objects.create(author=self.u_1.profile, title="1", content="test1")
        response = self.client.get("/posts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["posts"]), 1)
        self.assertEqual(response.data["posts"][0]["author"]["display_name"], "2haotianzhu")

    def test_get_many(self):
        Post.objects.create(author=self.u_1.profile, title="2", content="test2")
        Post.objects.create(author=self.u_1.profile, title="3", content="test3")
        response = self.client.get("/posts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["posts"]), 2)

    def test_get_post_by_id(self):
        Post.objects.create(author=self.u_1.profile, title="4", content="test4")
        the_id = Post.objects.get().pk
        path = "/posts/{}".format(the_id)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["posts"][0]["author"]["display_name"], "2haotianzhu")

    def test_get_auth_posts(self):
        # get post by auth

        # own
        p_5 = Post.objects.create(
            author=self.u_1.profile, title="5", content="test", visibility="PRIVATE"
        )
        p_5.visible_to.set([self.u_1.profile])

        # public
        Post.objects.create(author=self.u_5.profile, title="6", content="test", visibility="PUBLIC")
        # friends
        Post.objects.create(
            author=self.u_2.profile, title="7", content="test", visibility="FRIENDS"
        )
        # foaf
        Post.objects.create(author=self.u_4.profile, title="8", content="test", visibility="FOAF")

        # private can see
        p_10 = Post.objects.create(
            author=self.u_6.profile, title="10", content="test", visibility="PRIVATE"
        )
        p_10.visible_to.set([self.u_1.profile])

        # private cant see
        Post.objects.create(
            author=self.u_5.profile, title="9", content="test", visibility="PRIVATE"
        )
        response = self.client.get("/author/posts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "posts")
        self.assertEqual(len(response.data["posts"]), 5)

    def test_auth_post_a_post(self):
        data = {
            "query": "createPost",
            "post": {"title": "test", "content_type": "text/plain", "content": "some post content"},
        }
        response = self.client.post("/author/posts", data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "createPost")
        self.assertEqual(response.data["success"], True)
        self.assertEqual(Post.objects.all()[0].author.display_name, "2haotianzhu")

    def test_unlisted_cases(self):
        data1 = {
            "query": "createPost",
            "post": {
                "title": "unlisted True",
                "content_type": "text/plain",
                "content": "some post content",
                "unlisted": True,
            },
        }
        data2 = {
            "query": "createPost",
            "post": {
                "title": "unlisted False",
                "content_type": "text/plain",
                "content": "some post content",
                "unlisted": False,
            },
        }
        response = self.client.post("/author/posts", data1, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/author/posts", data2, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/posts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["posts"]), 1)
        self.assertEqual(response.data["posts"][0]["title"], "unlisted False")
        post = Post.objects.get(title="unlisted False")
        response = self.client.get("/posts/{}".format(post.id))
        self.assertEqual(response.status_code, 200)
        post = Post.objects.get(title="unlisted True")
        response = self.client.get("/posts/{}".format(post.id))
        self.assertEqual(response.status_code, 200)
        response = self.client.delete("/posts/{}".format(post.id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Post.objects.all()), 1)

    # def test_get_remote_foaf(self):
    #     # only can be test if local server is running ("http://127.0.0.1:5000")
    #     # if you need script of local server, please contact me (RAY)
    #     # simulate remote server ask the foaf post
    #
    #     # setup user
    #     credentials_remote_server = base64.b64encode(
    #         "{}:{}".format("RemoteServerB", "RemoteServerB").encode()
    #     ).decode()
    #     remote_client = Client(HTTP_AUTHORIZATION="Basic {}".format(credentials_remote_server))
    #
    #     # logined remote server s1
    #     s1_represent = User.objects.create(username="RemoteServerA")
    #     s1_represent.set_password("RemoteServerA")
    #     s1_represent.profile.url = "https://cmput404-front-A.herokuapp.com"
    #     s1_represent.save()
    #
    #     s1 = Server.objects.create(
    #         author=s1_represent,
    #         foreign_db_username="s1",
    #         foreign_db_password="111",
    #         url="https://cmput404-front-S1.herokuapp.com",
    #         endpoint="https://cmput404-front-S1.herokuapp.com/api",
    #     )
    #
    #     # logined remote server s2
    #     s2_represent = User.objects.create(username="RemoteServerB")
    #     s2_represent.set_password("RemoteServerB")
    #     s2_represent.profile.url = "http://127.0.0.1:5000"
    #     s2_represent.save()
    #
    #     s2 = Server.objects.create(
    #         author=s2_represent,
    #         foreign_db_username="s2",
    #         foreign_db_password="222",
    #         url="http://127.0.0.1:5000",
    #         endpoint="http://127.0.0.1:5000/api",
    #     )
    #
    #     # local user u1
    #     u1 = User.objects.create_user(username="testUser", first_name="test", last_name="user")
    #     u1.set_password("test")
    #     u1.profile.display_name = "testUser"
    #     u1.profile.url = u1.profile.get_full_id()
    #     u1.save()
    #
    #     # local user u2
    #     u2 = User.objects.create_user(username="6zhi", first_name="zhi", last_name="li")
    #     u2.profile.display_name = "zhili"
    #     u2.profile.url = u2.profile.get_full_id()
    #     u2.save()
    #
    #     # remote users in Server S1
    #     s1_u1 = UserProfile.objects.create(
    #         display_name="haotian",
    #         host=s1,
    #         url="https://cmput404-front-S1.herokuapp.com/author/1d698d25ff008f7538453c120f581471",
    #     )
    #
    #     s1_u2 = UserProfile.objects.create(
    #         display_name="aaa",
    #         host=s1,
    #         url="https://cmput404-front-S1.herokuapp.com/author/sdfsdfsdfsdfwerfsdfs342sdfgdsfgds",
    #     )
    #
    #     # remote users in Server S2
    #     s2_u1 = UserProfile.objects.create(
    #         display_name="localhost_test",
    #         host=s2,
    #         url="http://127.0.0.1:5000/author/1d698d25ff008f7538453c120f581471",
    #     )
    #
    #     Friend.objects.create(profile1=u1.profile, profile2=u2.profile)
    #     Friend.objects.create(profile1=u1.profile, profile2=s1_u1)
    #     Friend.objects.create(profile1=u2.profile, profile2=s1_u2)
    #     # Friend.objects.create(profile1=s1_u1, profile2=s2_u1)
    #     # Friend.objects.create(profile1=s1_u2, profile2=s2_u1)
    #
    #     foaf_post_1 = Post.objects.create(
    #         author=u1.profile,
    #         title="foaf test post 1",
    #         visibility="FOAF",
    #         unlisted=False
    #     )
    #
    #     foaf_post_2 = Post.objects.create(
    #         author=u1.profile,
    #         title="foaf test post 2",
    #         visibility="FOAF",
    #         unlisted=False
    #     )
    #
    #     foaf_post_3 = Post.objects.create(
    #         author=u2.profile,
    #         title="foaf test post 3",
    #         visibility="FOAF",
    #         unlisted=False
    #     )
    #
    #     post_list_1 = post_views.get_request_user_foaf_post_belong_local_author(
    #         request_user_full_id="http://127.0.0.1:5000/author/1d698d25ff008f7538453c120f581471",
    #         local_author_profile_id=u1.profile.id
    #     )
    #
    #     self.assertEqual(len(post_list_1), 2)
    #     # print([post.title for post in post_list])
    #     self.assertTrue(foaf_post_1 in post_list_1)
    #     self.assertTrue(foaf_post_2 in post_list_1)
    #
    #     post_list_2 = post_views.get_request_user_foaf_post(
    #         request_user_full_id="http://127.0.0.1:5000/author/1d698d25ff008f7538453c120f581471"
    #     )
    #     self.assertEqual(len(post_list_2), 3)
    #     self.assertTrue(foaf_post_1 in post_list_2)
    #     self.assertTrue(foaf_post_2 in post_list_2)
    #     self.assertTrue(foaf_post_3 in post_list_2)
    #
    #     # if need test here you have to change little bit code in post review
    #     # add foreign_user_url = request.META["headers"]["X-Request-User-ID"]  # RAY TEST
    #
    #     # headers = {"X-Request-User-ID": "http://127.0.0.1:5000/author/1d698d25ff008f7538453c120f581471"}
    #     # response = remote_client.get(
    #     #     "/author/{}/posts".format(u1.id),
    #     #     headers=headers,
    #     #     auth=('RemoteServerB', 'RemoteServerB')
    #     # )
    #     #
    #     #
    #     # print(response.status_code)
    #     # print(response.data)
    #
    #     # headers = {"X-Request-User-ID": "http://127.0.0.1:5000/author/1d698d25ff008f7538453c120f581471"}
    #     # response = remote_client.get(
    #     #     "/author/posts",
    #     #     headers=headers,
    #     #     auth=('RemoteServerB', 'RemoteServerB')
    #     # )
    #     # print(response.status_code)
    #     # print(response.data)
