
from django.db import models
from django.utils import timezone
from .user import UserProfile
from django.conf import settings


class Post(models.Model):
    '''
    author: User
    create_date: date
    last_modify_date: date
    comments: [Comment]
    '''
    class Meta:
        app_label = 'hyperion'

    CHOICES = (
        ('PUBLIC', 'PUBLIC'),
        ('FOAF', 'FOAF'),
        ('FRIENDS', 'FRIENDS'),
        ('PRIVATE', 'PRIVATE'),
        ('SERVERONLY', 'SERVERONLY'),
    )
    CONTENT_TYPES = (
        ('text/plain', 'text/plain'),
        ('text/markdown', 'text/markdown'),
        ('image/png;base64', 'image/png;base64'),
        ('image/jpeg;base64', 'image/jpeg;base64'),
        ('application/base64', 'application/base64'),
    )

    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='post_author')
    content = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    last_modify_date = models.DateTimeField(default=timezone.now)
    source = models.URLField(
        max_length=200,
        null=True,
        blank=True
    )
    origin = models.URLField(
        max_length=200,
        default=settings.HYPERION_HOSTNAME
    )
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPES,
        default='PUBLIC'
    )
    visibility = models.CharField(
        max_length=20,
        choices=CHOICES,
        default='text/plain'
    )
    visible_to = models.ManyToManyField(
        UserProfile,
        related_name='visible'
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return super().__str__()+' post: '+str(self.author.pk)

    def visible_to_me(self):
        self.visible_to.add(self.author)

    def visible_to_another_author(self, user_profile):
        self.visible_to.add(user_profile)

    def visible_to_host_friends(self):
        host_friends = self.author.get_friends(including='host')
        for host_frend in host_friends:
            self.visible_to.add(host_frend)

    def visible_to_my_friends(self):
        friends = self.author.get_friends()
        for friend in friends:
            self.visible_to.add(friend)

    def visible_to_friends_of_friends(self):
        friends_of_friends = self.author.get_friends_friends()
        for friend_of_friends in friends_of_friends:
            self.visible_to.add(friend_of_friends)

    def visible_to_public(self):
        self.visible_to.clear()

    def get_comments(self):
        return self.comments.all()
