
from datetime import datetime
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from hyperion.models import *
from django.contrib.auth.models import User
from django.test import TestCase

# python manage.py test -v=2 hyperion.models.tests_user_story

class UserStoryTestCase(TestCase):
    def setUp(self):
        self.u = User.objects.create(
            username='2haotianzhu',
            first_name='haotian',
            last_name='zhu')

    def test_1(self):
        # As an author I want to make posts.
        
        return
    def test_2(self):
        # As an author, posts I create can link to images.
        return

    def test_3(self):
        # As a server admin, images can be hosted on my server.
        return
    def test_4(self):
        # As an author, posts I create be private to me
        return
    def test_5(self):
        # As an author, posts I create be private to another author
        return
    def test_6(self):
        # As an author, posts I create be private to my friends
        return
    def test_8(self):
        # As an author, posts I create be private to friends of friends
        return
    def test_9(self):
        # As an author, posts I create be private to only friends on my host
        return
    def test_10(self):
        # As an author, posts I create can be public
        return
    def test_11(self):
        # As an author, posts I make can be in simple plain text
        return
    def test_12(self):
        # As an author, posts I make can be in markdown (commonMark is good)
        return
    def test_13(self):
        # As an author, I want a consistent identity per server
        return
    def test_14(self):
        # As a server admin, I want to host multiple authors on my server
        return
    def test_15(self):
        # As a server admin, I want to share or not share posts with users 
        # on other servers.
        return
    def test_16(self):
        # As a server admin, I want to share or not share images with
        #  users on other servers.
        return
    def test_17(self):
        #As an author, I want to pull in my github activity to my “stream”
        return
    def test_18(self):
        #As an author, I want to post posts to my “stream”
        return
    def test_19(self):
        #As an author, I want to delete my own posts.
        return
    def test_20(self):
        #As an author, I want to befriend local authors
        return
    def test_21(self):
        #As an author, I want to befriend remote authors
        return
    def test_22(self):
        # As an author, I want to feel safe about sharing images and 
        # posts with my friends – images should not publicly accessible
        #  without authentication.
        return
    def test_23(self):
        # As an author, I want un-befriend local and remote authors
        return
    def test_24(self):
        # As an author, I want to be able to use my web-browser to manage 
        # my profile
        return
    def test_25(self):
        # As an author, I want to be able to use my web-browser to 
        # manage/author my posts
        return
    def test_25(self):
        # As a server admin, I want to be able add, modify, and remove authors.
        return
    def test_26(self):
        # As a server admin, I want to be able allow users to sign up 
        # but require my OK to finally be on my server
        return
    def test_27(self):
        # As a server admin, I don’t want to do heavy setup to get the 
        # posts of my author’s friends.
        return
    def test_28(self):
        # As a server admin, I want a restful interface for most operations
        return
    def test_29(self):
        # As an author, other authors cannot modify my data
        return
    def test_30(self):
        # As an author, I want to comment on posts that I can access
        return
    def test_31(self):
        # As an author, my server will know about my friends
        return
    def test_32(self):
        # As an author, When I befriend someone it follows them, 
        # only when the other authors befriends me do I count as a real friend.
        return
    def test_33(self):
        #As an author, I want to know if I have friend requests.
        return
    def test_34(self):
        #As an author I should be able to browse the public posts of everyone
        return
    def test_35(self):
        # As an author I should be able to browse the posts of others
        # depending on my status
        return
    def test_36(self):
        # As a server admin, I want to be able to add nodes to share with
        return
    def test_37(self):
        # As a server admin, I want to be able to remove nodes and stop 
        # sharing with them.
        return
    def test_38(self):
        # As a server admin, I can limit nodes connecting to me via authentication.
        return
    def test_39(self):
        # As a server admin, node to node connections can be authenticated 
        # with HTTP Basic Auth
        return
    def test_40(self):
        # As a server admin, I can disable the node to node interfaces 
        # for connections that are not authenticated!
        return
    def test_41(self):
        # As an author, I want to be able to make posts that are unlisted, 
        # that are publicly shareable by URI alone (or for embedding images)        
        return