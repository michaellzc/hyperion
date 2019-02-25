from django.test import TestCase, Client
from django.contrib.auth.models import User
from hyperion.models import UserProfile, Friend, FriendRequest, Server
from hyperion.serializers import UserSerializer, UserProfileSerializer

import json
import copy
from urllib.parse import quote


class FriendViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # logined user u1
        cls.u1 = User.objects.create_user(
            username='testUser',
            first_name='test',
            last_name='user',
            password='test'
        )
        cls.u1.profile.display_name = "testUser"
        cls.u1.profile.url = cls.u1.profile.get_full_id()
        cls.u1.save()

        # local user u2 (friend with u1)
        cls.u2 = User.objects.create_user(
            username='6zhi',
            first_name='zhi',
            last_name='li'
        )
        cls.u2.profile.display_name = "zhili"
        cls.u2.profile.url = cls.u2.profile.get_full_id()
        cls.u2.save()

        # local user u3 (friend with u1)
        cls.u3 = User.objects.create_user(
            username='xinlei',
            first_name='xinlei',
            last_name='chen'
        )
        cls.u3.profile.display_name = "raymundo"
        cls.u3.profile.url = cls.u3.profile.get_full_id()
        cls.u3.save()

        # local user u4 (not friend with u1)
        cls.u4 = User.objects.create_user(
            username='gorilla',
            first_name='go',
            last_name='rilla'
        )
        cls.u4.profile.display_name = "gorilla"
        cls.u4.profile.url = cls.u4.profile.get_full_id()
        cls.u4.save()

        # remote user fu1
        s1 = Server.objects.create(
            name="https://cmput404-front-t2.herokuapp.com"
        )
        cls.fu1 = UserProfile.objects.create(
            display_name="haotian",
            host=s1,
            url="https://cmput404-front-t2.herokuapp.com/author/1d698d25ff008f7538453c120f581471",
        )

        Friend.objects.create(profile1=cls.u1.profile, profile2=cls.u2.profile)
        Friend.objects.create(profile1=cls.u1.profile, profile2=cls.u3.profile)
        Friend.objects.create(profile1=cls.u1.profile, profile2=cls.fu1)
        # Friend.objects.create(profile1=cls.u2.profile, profile2=cls.u3.profile)

    @staticmethod
    def _check_list_equal(l1, l2):
        return len(l1) == len(l2) and sorted(l1) == sorted(l2)

    def test_friend_list_get(self):
        self.client.login(username='testUser', password='test')
        self.assertTrue(self.u1.is_authenticated)

        response = self.client.get('/author/{}/friends'.format(self.u1.id))
        self.assertEqual(response.status_code, 200)
        friends = list(self.u1.profile.get_friends())
        serializer = UserProfileSerializer(friends,
                                           many=True,
                                           context={'fields': ['id', "host", "display_name", "url"]})
        content = {"query": "friends", "count": len(friends), "author": serializer.data}
        self.assertEqual(response.data, json.dumps(content))
        # print(response.data)
        self.client.logout()

    def test_friend_list_post(self):
        post_body = {
            "query": "friends",
            "author": "{}".format(self.u1.id),
            "authors": [
                # local user (friend with u1)
                "https://cmput404-front.herokuapp.com/author/{}".format(self.u2.id),
                # remote user (friend with u1)
                self.fu1.url,
                # local user (not friend with u1)
                "https://cmput404-front.herokuapp.com/author/{}".format(self.u4.id),
                # local user (not exist)
                "https://cmput404-front.herokuapp.com/author/{}".format(100),
                # remote user (not in our system)
                "https://cmput404-front-t2.herokuapp.com/author/100"
            ]
        }

        # https://stackoverflow.com/questions/8583290/sending-json-using-the-django-test-client
        response = self.client.post("/author/{}/friends".format(self.u1.id), post_body, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result_body = copy.deepcopy(post_body)
        result_body["authors"].remove("https://cmput404-front.herokuapp.com/author/{}".format(self.u4.id))
        result_body["authors"].remove("https://cmput404-front.herokuapp.com/author/{}".format(100))
        result_body["authors"].remove("https://cmput404-front-t2.herokuapp.com/author/100")
        # print(json.loads(response.data))

        response_data = json.loads(response.data)
        self.assertTrue(self._check_list_equal(result_body["authors"], response_data["authors"]))
        self.assertEqual(response_data["query"], "friends")
        self.assertEqual(response_data["author"], str(self.u1.id))

    def test_check_friendship(self):
        # check remote friend (not friend with author1)
        url = "/author/{}/friends/cmput404-front-t3.herokuapp.com/author/ae345d54-75b4-431b-adb2-fb6b9e547891"\
            .format(self.u1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['friends'], False)
        # print(response.data)

        # check remote friend (friend with author1)
        url = "/author/{}/friends/cmput404-front-t2.herokuapp.com/author/1d698d25ff008f7538453c120f581471"\
            .format(self.u1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['friends'], True)

        # check local friend (not friend with author1)
        url = "/author/{}/friends/cmput404-front.herokuapp.com/author/{}".format(self.u1.id, self.u4.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['friends'], False)

        # check local friend (friend with author1)
        url = "/author/{}/friends/cmput404-front.herokuapp.com/author/{}".format(self.u1.id, self.u2.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['friends'], True)

    def test_friend_request_post(self):
        u1_serializer = UserProfileSerializer(self.u1.profile,
                                              context={'fields': ['id', "host", "display_name", "url"]})

        # scenario #1 u4 send request to u1
        u4_serializer = UserProfileSerializer(self.u4.profile,
                                              context={'fields': ['id', "host", "display_name", "url"]})

        # print(type(author_serializer.data))
        post_body = {
            "query": "friendrequest",
            "author": u4_serializer.data,
            "friend": u1_serializer.data,
        }
        # print(json.dumps(post_body))
        response = self.client.post("/friendrequest", post_body, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(FriendRequest.objects.get(to_profile=self.u1.profile).from_profile, self.u4.profile)
        author_list = list(UserProfile.objects.filter(
            id__in=list(FriendRequest.objects.filter(to_profile=self.u1.profile)
                        .values_list('from_profile', flat=True))))
        self.assertTrue(self.u4.profile in author_list)

        # scenario #2 remote fu1 (trusted server and exist profile) send request to u1
        fu1_serializer = UserProfileSerializer(self.fu1,
                                               context={'fields': ['id', "host", "display_name", "url"]})
        post_body = {
            "query": "friendrequest",
            "author": fu1_serializer.data,
            "friend": u1_serializer.data,
        }
        response = self.client.post("/friendrequest", post_body, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(FriendRequest.objects.get(to_profile=self.u1.profile).from_profile, self.fu1)
        # TODO: ?? why only get id from values_list
        author_list = list(UserProfile.objects.filter(
            id__in=list(FriendRequest.objects.filter(to_profile=self.u1.profile)
                        .values_list('from_profile', flat=True))))
        self.assertTrue(self.fu1 in author_list)

        # scenario #3 remote user (untrusted server and non-exist profile) send request to u1
        post_body = {
            "query": "friendrequest",
            "author": {
                "id": "https://cmput404-front-t10.herokuapp.com/author/de305d54-75b4-431b-adb2-eb6b9e546013",
                "host": "https://cmput404-front-t10.herokuapp.com",
                "display_name": "user from untrusted server",
                "url": "https://cmput404-front-t10.herokuapp.com/author/de305d54-75b4-431b-adb2-eb6b9e546013",
            },
            "friend": u1_serializer.data
        }
        response = self.client.post("/friendrequest", post_body, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # print(response.data)

        # scenario #4 remote user (trusted server and non-exist profile) send request to u1
        post_body = {
            "query": "friendrequest",
            "author": {
                "id": "https://cmput404-front-t2.herokuapp.com/author/de305d54-75b4-431b-adb2-eb6b9e546013",
                "host": "https://cmput404-front-t2.herokuapp.com",
                "display_name": "remote_user2",
                "url": "https://cmput404-front-t2.herokuapp.com/author/de305d54-75b4-431b-adb2-eb6b9e546013",
            },
            "friend": u1_serializer.data
        }
        response = self.client.post("/friendrequest", post_body, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        fu2 = UserProfile.objects.get(url=post_body['author']['url'])
        author_list = list(UserProfile.objects.filter(
            id__in=list(FriendRequest.objects.filter(to_profile=self.u1.profile)
                        .values_list('from_profile', flat=True))))
        self.assertTrue(fu2 in author_list)

    def test_friend_request_get(self):
        # send request firstly
        u1_serializer = UserProfileSerializer(self.u1.profile,
                                              context={'fields': ['id', "host", "display_name", "url"]})

        # scenario #1 u4 send request to u1
        u4_serializer = UserProfileSerializer(self.u4.profile,
                                              context={'fields': ['id', "host", "display_name", "url"]})

        # print(type(author_serializer.data))
        post_body = {
            "query": "friendrequest",
            "author": u4_serializer.data,
            "friend": u1_serializer.data,
        }
        self.client.post("/friendrequest", post_body, content_type='application/json')

        # scenario #2 remote fu1 (trusted server and exist profile) send request to u1
        fu1_serializer = UserProfileSerializer(self.fu1,
                                               context={'fields': ['id', "host", "display_name", "url"]})
        post_body = {
            "query": "friendrequest",
            "author": fu1_serializer.data,
            "friend": u1_serializer.data,
        }
        self.client.post("/friendrequest", post_body, content_type='application/json')

        # then test get
        response = self.client.get('/friendrequest')
        self.assertEqual(response.status_code, 401)
        self.client.login(username='testUser', password='test')
        self.assertTrue(self.u1.is_authenticated)

        response = self.client.get('/friendrequest')
        self.assertEqual(response.status_code, 200)
        # print(response.data)
        self.client.logout()

