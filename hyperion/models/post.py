# pylint: disable=no-member

from django.db import models
from django.utils import timezone
from django.conf import settings
from hyperion.models.user import UserProfile


class Post(models.Model):
    """
    author: User
    create_date: date
    last_modify_date: date
    comments: [Comment]
    """

    class Meta:
        app_label = "hyperion"

    CHOICES = (
        ("PUBLIC", "PUBLIC"),
        ("FOAF", "FOAF"),
        ("FRIENDS", "FRIENDS"),
        ("PRIVATE", "PRIVATE"),
        ("SERVERONLY", "SERVERONLY"),
    )
    CONTENT_TYPES = (
        ("text/plain", "text/plain"),
        ("text/markdown", "text/markdown"),
        ("image/png;base64", "image/png;base64"),
        ("image/jpeg;base64", "image/jpeg;base64"),
        ("application/base64", "application/base64"),
    )

    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="post_author"
    )
    content = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    last_modify_date = models.DateTimeField(default=timezone.now)
    content_type = models.CharField(
        max_length=20, choices=CONTENT_TYPES, default="text/plain"
    )
    visibility = models.CharField(max_length=20, choices=CHOICES, default="PUBLIC")
    visible_to = models.ManyToManyField(UserProfile, related_name="visible")
    description = models.TextField(null=True, blank=True)
    unlisted = models.BooleanField(default=False)

    def __str__(self):
        return super().__str__() + " post: " + str(self.author.pk)

    def visible_to_me(self):
        self.visible_to.add(self.author)

    def visible_to_another_author(self, user_profile):
        self.visible_to.add(user_profile)
    def post_accessible(self,post,user_profile):
        if post.visibility == 'FRIENDS':
            friends = user_profile.get_friends()
            if post.author in friends:
                return True
        elif post.visibility == 'FOAF':
            friends_of_friends = user_profile.get_friends_friends()
            if post.author in friends_of_friends:
                return True
        elif post.visibility == 'PUBLIC':
            return True    
        elif post.visibility == 'PRIVATE' and user_profile in post.visible_to.all():
            return True 
        return False
    @staticmethod
    def visible_to_friends(user_profile):
        friends = user_profile.get_friends()
        all_post = Post.objects.all()
        friend_posts = []

        for post in all_post:
            if post.author in friends and post.visibility == "FRIENDS":
                friend_posts.append(post)
        return friend_posts

    @staticmethod
    def visible_to_friends_of_friends(user_profile):
        friends_of_friends = user_profile.get_friends_friends()
        all_post = Post.objects.all()
        foaf_posts = []

        for post in all_post:
            if post.author in friends_of_friends and post.visibility == "FOAF":
                foaf_posts.append(post)
        return foaf_posts

    @staticmethod
    def visible_to_public():
        all_post = Post.objects.all()
        public_posts = []

        for post in all_post:
            if post.visibility == "PUBLIC":
                public_posts.append(post)
        return public_posts

    @staticmethod
    def visible_to_private(user_profile):
        all_post = Post.objects.all()
        private_posts = []
        for post in all_post:
            if post.visibility == "PRIVATE" and user_profile in post.visible_to.all():
                private_posts.append(post)
        return private_posts

    def get_comments(self):
        return self.comments.all()

    def get_source(self):
        host_name = settings.HYPERION_HOSTNAME
        return "{}/posts/{}".format(host_name, self.id)

    def set_private_to_host_friend(self):
        self.visibility = "PRIVATE"
        friends = [u.id for u in self.author.get_friends(including="host")]
        self.visible_to.set(friends)
