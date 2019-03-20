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
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="post_author")
    content = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    last_modify_date = models.DateTimeField(default=timezone.now)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES, default="text/plain")
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

    def is_accessible(self, post, user_profile):
        if user_profile == post.author:
            return True
        else:
            if post.visibility == "FRIENDS":
                friends = user_profile.get_friends()
                if post.author in friends:
                    return True
            elif post.visibility == "FOAF":
                friends_of_friends = user_profile.get_friends_friends()
                if post.author in friends_of_friends:
                    return True
            elif post.visibility == "PUBLIC":
                return True
            elif post.visibility == "PRIVATE" and user_profile in post.visible_to.all():
                return True
            return False

    @staticmethod
    def not_own_posts_visible_to_me(user_profile):
        visible_post = []
        friends = user_profile.get_friends()
        friends_of_friends = user_profile.get_friends_friends()
        all_post = Post.objects.all()

        for post in all_post:
            if post.visibility == "FRIENDS" and post.author in friends:
                visible_post.append(post)
            elif post.visibility == "FOAF" and post.author in friends_of_friends:
                visible_post.append(post)
            elif post.visibility == "PRIVATE" and user_profile in post.visible_to.all():
                visible_post.append(post)
        return visible_post

    def get_comments(self):
        return self.comments.all()

    def get_source(self):
        host_name = settings.HYPERION_HOSTNAME
        return "{}/posts/{}".format(host_name, self.id)

    def set_private_to_host_friend(self):
        self.visibility = "PRIVATE"
        friends = [u.id for u in self.author.get_friends(including="host")]
        self.visible_to.set(friends)
