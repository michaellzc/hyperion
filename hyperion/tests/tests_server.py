
from datetime import datetime
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from hyperion.models import Server, UserProfile, Friend
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.exceptions import ValidationError


# python manage.py test -v=2 hyperion.models.tests_server

class ServerTestCase(TestCase):
    def setup(self):
        pass

    def test_create_server(self):
        s1 = Server.objects.create(name='hhahaha')
        self.assertEquals(Server.objects.get().name, 'hhahaha')

    def test_our_user_profile(self):
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
        s1 = Server.objects.create(name='hhahaha')
        # raise error if  no host and no user
        self.assertRaises(
            ValidationError,
            UserProfile.objects.create,
            display_name='yangww1'
        )
        fu1 = UserProfile.objects.create(
            display_name='yangww1',
            host=s1
        )
        fu2 = UserProfile.objects.create(
            display_name='ggyanh2',
            host=s1
        )

        # add friends
        Friend.objects.create(profile1=fu1, profile2=u1.profile)
        self.assertEquals(list(u1.profile.get_friends()), [fu1])

    def test_user_get_method(self):
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
        s1 = Server.objects.create(name='hhahaha')

        fu1 = UserProfile.objects.create(
            display_name='yangww1',
            host=s1
        )
        fu2 = UserProfile.objects.create(
            display_name='ggyanh2',
            host=s1
        )
        Friend.objects.create(profile1=fu1, profile2=u1.profile)
        Friend.objects.create(profile1=u2.profile, profile2=u1.profile)
        Friend.objects.create(profile1=fu1, profile2=u2.profile)
        Friend.objects.create(profile1=fu2, profile2=u1.profile)

        l1 = list(u1.profile.get_friends())
        l1.sort(key=lambda x: x.pk)
        l2 = [fu1, fu2, u2.profile]

        l2.sort(key=lambda x: x.pk)

        self.assertEquals(l1, l2)

        l1 = list(u1.profile.get_friends(including='all'))
        l1.sort(key=lambda x: x.pk)

        self.assertEquals(l1, l2)
        self.assertEquals(
            list(u1.profile.get_friends(including='host')),
            [u2.profile]
        )
        l1 = list(u1.profile.get_friends(including='foreign'))
        l1.sort(key=lambda x: x.pk)
        l2 = [fu1, fu2]
        l2.sort(key=lambda x: x.pk)
        self.assertEquals(l1, l2)

        self.assertRaises(
            ValidationError,
            Friend.objects.create,
            profile1=fu2,
            profile2=fu1
        )
