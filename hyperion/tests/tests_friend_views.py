from django.test import TestCase, Client
from django.contrib.auth.models import User
from hyperion.models import UserProfile, Friend, FriendRequest
from hyperion.serializers import UserSerializer, UserProfileSerializer

import json

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

        # local user u2
        cls.u2 = User.objects.create_user(
            username='6zhi',
            first_name='zhi',
            last_name='li'
        )
        cls.u2.profile.display_name = "zhili"
        cls.u2.profile.url = cls.u2.profile.get_full_id()

        # local user u3
        cls.u3 = User.objects.create_user(
            username='xinlei',
            first_name='xinlei',
            last_name='chen'
        )
        cls.u3.profile.display_name = "raymundo"
        cls.u3.profile.url = cls.u3.profile.get_full_id()

        Friend.objects.create(profile1=cls.u1.profile, profile2=cls.u2.profile)
        Friend.objects.create(profile1=cls.u1.profile, profile2=cls.u3.profile)

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
        print(response.data)
        # ?? can not get url
        # print(self.u2.profile.url)
        self.client.logout()
