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
    def setUp(self):
        s_user = User.objects.create_user(username="other")
        self.s1 = Server.objects.create(author=s_user)

    def test_our_user_profile(self):
        u1 = User.objects.create(username="2haotianzhu", first_name="haotian", last_name="zhu")
        u2 = User.objects.create(username="1yutianzhang", first_name="yutian", last_name="zhang")
        u3 = User.objects.create(username="3zhili", first_name="zhi", last_name="li")
        # raise error if  no host and no user
        self.assertRaises(ValidationError, UserProfile.objects.create, display_name="yangww1")
        fu1 = UserProfile.objects.create(display_name="yangww1", host=self.s1)
        fu2 = UserProfile.objects.create(display_name="ggyanh2", host=self.s1)

        # add friends
        Friend.objects.create(profile1=fu1, profile2=u1.profile)
        self.assertEquals(list(u1.profile.get_friends()), [fu1])

    def test_user_get_method(self):
        u1 = User.objects.create(username="2haotianzhu", first_name="haotian", last_name="zhu")
        u1.profile.url = "https://cmput404-front-t2.herokuapp.com/author/1"
        u1.save()
        u2 = User.objects.create(username="1yutianzhang", first_name="yutian", last_name="zhang")
        u2.profile.url = "https://cmput404-front-t2.herokuapp.com/author/2"
        u2.save()
        fu1 = UserProfile.objects.create(
            display_name="yangww1",
            host=self.s1,
            url="https://cmput404-front-t2.herokuapp.com/author/dfsw424sdfs",
        )
        fu2 = UserProfile.objects.create(
            display_name="ggyanh2",
            host=self.s1,
            url="https://cmput404-front-t2.herokuapp.com/author/sdfsfsw423sdfdssdfs",
        )
        fu2_dup = UserProfile.objects.create(
            display_name="ggyanh2",
            host=self.s1,
            url="https://cmput404-front-t2.herokuapp.com/author/sdfsfsw423sdfdssdfs",
        )
        Friend.objects.create(profile1=fu1, profile2=u1.profile)
        Friend.objects.create(profile1=u2.profile, profile2=u1.profile)
        Friend.objects.create(profile1=fu1, profile2=u2.profile)
        Friend.objects.create(profile1=fu2, profile2=u1.profile)
        Friend.objects.create(profile1=fu2_dup, profile2=u1.profile)

        l1 = list(u1.profile.get_friends())
        # print(l1, "xxxx")
        l1.sort(key=lambda x: x.pk)
        l2 = [fu1, fu2, u2.profile]

        l2.sort(key=lambda x: x.pk)
        # print(l2, "yyyy")
        self.assertEquals(l1, l2)

        l1 = list(u1.profile.get_friends(including="all"))
        l1.sort(key=lambda x: x.pk)

        self.assertEquals(l1, l2)
        self.assertEquals(list(u1.profile.get_friends(including="host")), [u2.profile])
        l1 = list(u1.profile.get_friends(including="foreign"))
        l1.sort(key=lambda x: x.pk)
        l2 = [fu1, fu2]
        l2.sort(key=lambda x: x.pk)
        self.assertEquals(l1, l2)

        self.assertRaises(ValidationError, Friend.objects.create, profile1=fu2, profile2=fu1)
