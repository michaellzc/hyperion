from datetime import datetime
from django.db import models
from django.utils import timezone
from ..models.post import Post
from ..models.user import UserProfile
from ..models.user import Friend
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.exceptions import ValidationError


class PostTestCase(TestCase):

    def setUp(self):
        self.u1 = User.objects.create(
                username='2haotianzhu',
                first_name='haotian',
                last_name='zhu')
        self.u2 = User.objects.create(
                username='1yutianzhang',
                first_name='yutian',
                last_name='zhang',
            )
        self.u3 = User.objects.create(
                username='3zhili',
                first_name='zhi',
                last_name='li')

        self.u4 = User.objects.create(
                username='2zhili',
                first_name='zhi',
                last_name='li')

        self.u5 = User.objects.create(
                username='1zhili',
                first_name='zhi',
                last_name='li')

        Friend.objects.create(profile1=self.u1.profile, profile2=self.u2.profile)
        Friend.objects.create(profile1=self.u1.profile, profile2=self.u4.profile)
        Friend.objects.create(profile1=self.u2.profile, profile2=self.u3.profile)

    # def test_private_to_me(self):
    #     p = Post.objects.create(
    #     author=self.u1.profile,
    #     title="u1_private",
    #     content="test1"
    #     )
    #     p.visible_to_me()
    #     self.assertEquals(list(p.visibleTo.all()), [self.u1.profile])

    def test_private_to_another_author(self):
        User = self.u5.profile
        p = Post.objects.create(
        author=self.u1.profile,
        title="u1_fof",
        content="test3"
        )  
        p.visible_to_me()
        p.visible_to_another_author(User)
        self.assertEquals(list(p.visibleTo.all()),[self.u1.profile, self.u5.profile])

    # # def test_private_to_my_friends(self):
    # #     p = Post.objects.create(
    # #     author = self.u1.profile,
    # #     titile = "u1_private_to_my_friends",
    # #     content = "test5" ,
    # #     )
    # #     p.visible_to_my_friends()
    # #     self.assertEquals(list(p.visibleTo.all()),[self.u2])

    def test_private_to_friends_of_friends(self):
        p = Post.objects.create(
        author=self.u1.profile,
        title="u1_fof",
        content="test3"
        )
        p.visible_to_me()
        p.visible_to_friends_of_friends()
        self.assertEquals(list(p.visibleTo.all()),[self.u1.profile,self.u3.profile])

    def test_private_to_host_friends(self):  
        p = Post.objects.create(
        author=self.u1.profile,
        title= "u1_host_friends",
        content="test2"
        )
        p.visible_to_me()
        p.visible_to_host_friends()
        self.assertEquals(list(p.visibleTo.all()),[self.u1.profile, self.u2.profile ,self.u4.profile])

    def test_public(self):
        p = Post.objects.create(
        author=self.u1.profile,
        title="u1_public",
        content="test4"
        )
        p.visible_to_me()
        p.visible_to_public()
        self.assertEquals(list(p.visibleTo.all()),[]
        )
