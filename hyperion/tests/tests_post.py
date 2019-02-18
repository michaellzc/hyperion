from django.test import TestCase
from django.contrib.auth.models import User
from ..models.post import Post
from ..models.user import Friend
# from django.core.exceptions import ValidationError


class PostTestCase(TestCase):

    def setUp(self):
        self.u_1 = User.objects.create(
            username='2haotianzhu',
            first_name='haotian',
            last_name='zhu'
        )

        self.u_2 = User.objects.create(
            username='1yutianzhang',
            first_name='yutian',
            last_name='zhang',
        )

        self.u_3 = User.objects.create(
            username='3zhili',
            first_name='zhi',
            last_name='li'
        )

        self.u_4 = User.objects.create(
            username='2zhili',
            first_name='zhi',
            last_name='li'
        )

        self.u_5 = User.objects.create(
            username='1zhili',
            first_name='zhi',
            last_name='li'
        )

        Friend.objects.create(profile1=self.u_1.profile, profile2=self.u_2.profile)
        Friend.objects.create(profile1=self.u_1.profile, profile2=self.u_4.profile)
        Friend.objects.create(profile1=self.u_2.profile, profile2=self.u_3.profile)

    def test_private_to_me(self):
        post = Post.objects.create(
            author=self.u_1.profile,
            title="u1_private",
            content="test1"
        )
        post.visible_to_me()
        self.assertEqual(list(post.visible_to.all()), [self.u_1.profile])

    def test_private_to_another_author(self):
        user_profile = self.u_5.profile
        post = Post.objects.create(
            author=self.u_1.profile,
            title="u1_fof",
            content="test3"
        )
        post.visible_to_me()
        post.visible_to_another_author(user_profile)
        self.assertEqual(list(post.visible_to.all()),[self.u_1.profile, self.u_5.profile])

    # # def test_private_to_my_friends(self):
    # #     p = Post.objects.create(
    # #     author = self.u1.profile,
    # #     titile = "u1_private_to_my_friends",
    # #     content = "test5" ,
    # #     )
    # #     p.visible_to_my_friends()
    # #     self.assertEquals(list(p.visible_to.all()),[self.u2])

    def test_private_to_friends_of_friends(self):
        post = Post.objects.create(
            author=self.u_1.profile,
            title="u1_fof",
            content="test3"
        )
        post.visible_to_me()
        post.visible_to_friends_of_friends()
        self.assertEqual(list(post.visible_to.all()), [self.u_1.profile, self.u_3.profile])

    def test_private_to_host_friends(self):
        post = Post.objects.create(
            author=self.u_1.profile,
            title="u1_host_friends",
            content="test2"
        )
        post.visible_to_me()
        post.visible_to_host_friends()
        self.assertEqual(list(post.visible_to.all()), \
            [self.u_1.profile, self.u_2.profile, self.u_4.profile])

    def test_public(self):
        post = Post.objects.create(
            author=self.u_1.profile,
            title="u1_public",
            content="test4"
            )
        post.visible_to_me()
        post.visible_to_public()
        self.assertEqual(list(post.visible_to.all()), [])
