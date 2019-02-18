
from django.db import models
from django.utils import timezone
from .user import UserProfile


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
        ('1', 'PUBLIC'),
        ('2', 'FOAF'),
        ('3', 'FRIENDS'),
        ('4', 'PRIVATE'),
        ('5', 'SERVERONLY'),
    )

    title = models.CharField(max_length=100)
    author = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='post_author')
    content = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    last_modify_date = models.DateTimeField(default=timezone.now)
    visibility = models.CharField(max_length=1, choices=CHOICES, default='1')
    visible_to = models.ManyToManyField(
        UserProfile,
        # need to be fixed later
        # on_delete=models.ForeignKey('Post', on_delete=models.CASCADE),
        related_name='visible'
    )

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
