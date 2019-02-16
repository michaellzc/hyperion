
from datetime import datetime
from django.db import models
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from hyperion.models.user import UserProfile, Friend, FriendRequest




# python manage.py test -v=2 hyperion.tests.tests_user

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
            Friend.objects.create,
            profile1=u1.profile,
            profile2=u1.profile)

        # profile1.id is always < profile2.id
        if u1.profile.id <= u2.profile.id:
            left = u1.username
            right = u2.username
        else:
            left = u2.username
            right = u1.username

        Friend.objects.create(profile1=u1.profile, profile2=u2.profile)
        self.assertEquals(Friend.objects.get().profile1.author.username, left)
        self.assertEquals(Friend.objects.get().profile2.author.username, right)

        # get friends by calling profile's method get_friends
        u1_friends = u1.profile.get_friends()

        self.assertEquals(list(u1_friends), [u2.profile])

        Friend.objects.create(profile1=u1.profile, profile2=u3.profile)
        Friend.objects.create(profile1=u2.profile, profile2=u3.profile)

        self.assertEquals(list(u1.profile.get_friends()), [u2.profile, u3.profile])
        self.assertEquals(list(u2.profile.get_friends()), [u1.profile, u3.profile])
        self.assertEquals(list(u3.profile.get_friends()), [u1.profile, u2.profile])

        # test delete
        u1.delete()
        self.assertEquals(len(UserProfile.objects.all()), 2)
        self.assertEquals(list(u2.profile.get_friends()), [u3.profile])
        self.assertEquals(list(u3.profile.get_friends()), [u2.profile])

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
        u1.profile.send_friend_request(u2.profile)
        self.assertEquals(FriendRequest.objects.get().from_profile, u1.profile)
        self.assertEquals(FriendRequest.objects.get().to_profile, u2.profile)

        # u2 accepts
        u2.profile.accept_friend_request(u1.profile)
        self.assertEquals(list(FriendRequest.objects.all()), [])
        self.assertEquals(list(u1.profile.get_friends()), [u2.profile])
        self.assertEquals(list(u2.profile.get_friends()), [u1.profile])

        # u1 tries to add u3
        u1.profile.send_friend_request(u3.profile)
        self.assertEquals(FriendRequest.objects.get().from_profile, u1.profile)
        self.assertEquals(FriendRequest.objects.get().to_profile, u3.profile)

        # u3 declines
        u3.profile.decline_friend_request(u1.profile)
        self.assertEquals(list(FriendRequest.objects.all()), [])
        self.assertEquals(list(u1.profile.get_friends()), [u2.profile])
        self.assertEquals(list(u3.profile.get_friends()), [])

    def test_friends_friends(self):
        u1 = User.objects.create(
            username='2haotianzhu',
            first_name='haotian',
            last_name='zhu'
        )
        u2 = User.objects.create(
            username='1yutianzhang',
            first_name='yutian',
            last_name='zhang',
        )
        u3 = User.objects.create(
            username='3zhili',
            first_name='zhi',
            last_name='li'
        )
        Friend.objects.create(profile1=u1.profile, profile2=u2.profile)
        Friend.objects.create(profile1=u2.profile, profile2=u3.profile)
        self.assertEquals(
            list(u1.profile.get_friends_friends()), [u3.profile]
        )

        Friend.objects.create(profile1=u1.profile, profile2=u3.profile)
        self.assertEquals(
            list(u1.profile.get_friends_friends()), []
        )
