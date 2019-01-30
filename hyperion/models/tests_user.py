
from datetime import datetime
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from .user import UserProfile, UserToUser, FriendRequest
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.exceptions import ValidationError


# python manage.py test -v=2 hyperion.models.tests_user

class UserTestCase(TestCase):
    def setup(self):
        pass

    def test_create_userprofile(self):
        # test when we create user, if auto create user profile
        u1 = User.objects.create(username='c', first_name='a', last_name='b')

        self.assertEquals(len(UserProfile.objects.all()), 1)
        user_profile = UserProfile.objects.get()
        self.assertEquals(user_profile.author.username, 'c')
        self.assertEquals(user_profile.author.first_name, 'a')
        self.assertEquals(user_profile.author.last_name, 'b')

    def test_friends(self):
        u1 = User.objects.create(
            username='2haotianzhu',
            first_name='haotian',
            last_name='zhu')
        u2 = User.objects.create(
            username='1yutianzhang',
            first_name='yutian',
            last_name='zhang',
        )
        u3 = User.objects.create(
            username='3zhili',
            first_name='zhi',
            last_name='li')

        # you can not be a friend of yourself
        self.assertRaises(
            ValidationError,
            UserToUser.objects.create,
            user1=u1,
            user2=u1)

        # user1.username is always < user2.username
        UserToUser.objects.create(user1=u1, user2=u2)
        self.assertEquals(UserToUser.objects.get().user1.username, '1yutianzhang')
        self.assertEquals(UserToUser.objects.get().user2.username, '2haotianzhu')

        # get friends by calling profile's method get_friends
        u1_friends = u1.profile.get_friends()

        self.assertEquals(list(u1_friends), [u2])

        UserToUser.objects.create(user1=u1, user2=u3)
        UserToUser.objects.create(user1=u2, user2=u3)

        self.assertEquals(list(u1.profile.get_friends()), [u2, u3])
        self.assertEquals(list(u2.profile.get_friends()), [u1, u3])
        self.assertEquals(list(u3.profile.get_friends()), [u1, u2])

        # test delete
        u1.delete()
        self.assertEquals(len(UserProfile.objects.all()), 2)
        self.assertEquals(list(u2.profile.get_friends()), [u3])
        self.assertEquals(list(u3.profile.get_friends()), [u2])

    def test_friend_request(self):
        u1 = User.objects.create(
            username='2haotianzhu',
            first_name='haotian',
            last_name='zhu')
        u2 = User.objects.create(
            username='1yutianzhang',
            first_name='yutian',
            last_name='zhang',
        )
        u3 = User.objects.create(
            username='3zhili',
            first_name='zhi',
            last_name='li')

        # u1 tries to add u2
        u1.profile.send_friend_request(u2)
        self.assertEquals(FriendRequest.objects.get().from_user, u1)
        self.assertEquals(FriendRequest.objects.get().to_user, u2)

        # u2 accepts
        u2.profile.accept_friend_request(u1)
        self.assertEquals(list(FriendRequest.objects.all()), [])
        self.assertEquals(list(u1.profile.get_friends()), [u2])
        self.assertEquals(list(u2.profile.get_friends()), [u1])

        # u1 tries to add u3
        u1.profile.send_friend_request(u3)
        self.assertEquals(FriendRequest.objects.get().from_user, u1)
        self.assertEquals(FriendRequest.objects.get().to_user, u3)

        # u3 declines
        u3.profile.decline_friend_request(u1)
        self.assertEquals(list(FriendRequest.objects.all()), [])
        self.assertEquals(list(u1.profile.get_friends()), [u2])
        self.assertEquals(list(u3.profile.get_friends()), [])
