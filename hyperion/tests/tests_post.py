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

    def test_set_private_to_host_friend(self):
        p = Post.objects.create(
            author=self.u_1.profile, title="1", content="test1")
        p.set_private_to_host_friend()
        self.assertEquals(p.visibility, 'PRIVATE')
        self.assertEquals(len(p.visible_to), 2)

                