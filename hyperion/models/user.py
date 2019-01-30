
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    '''
    Attributes:
        author: User
        display_name:
        website:
        bio:
    methods:
        get_friends: return QuerySet of User 
        send_friend_request: create FriendRequest
        accept_friend_request: delete FriendRequest and create UserToUser
        decline_friend_request: delete FriendRequest

    '''
    class Meta:
        app_label = 'hyperion'

    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile')
    display_name = models.CharField(max_length=20)
    website = models.URLField(verbose_name="personal website", blank=True)
    bio = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return super().__str__()+' user: '+str(self.author.pk)

    def get_friends(self):
        # return queryset of all author's friends via UserToUser
        return User.objects.filter(friends__user1=self.author) | \
            User.objects.filter(friends_of__user2=self.author)

    def send_friend_request(self, to_user):
        # update FriendRequest
        # to_user is User object
        from hyperion.models import FriendRequest
        FriendRequest.objects.create(
            from_user=self.author, to_user=to_user)
        return

    def accept_friend_request(self, from_user):
        # if there is a request
        # from_user is User object
        from hyperion.models import UserToUser
        query = FriendRequest.objects.get(
            from_user=from_user, to_user=self.author)
        if query:
            UserToUser.objects.create(user1=self.author, user2=from_user)
            query.delete()
        return

    def decline_friend_request(self, from_user):
        # if there is a request, remove it
        query = FriendRequest.objects.get(
            from_user=from_user, to_user=self.author)
        if query:
            query.delete()
        return


# set signal for auto-create authorProfile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(author=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class UserToUser(models.Model):
    '''
    link table to track user's friends
    '''

    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friends_of')
    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friends')

    class Meta:
        app_label = 'hyperion'
        unique_together = ('user1', 'user2',)

    def __str__(self):
        return super().__str__()+' {} <-> {} '.format(
            self.user1.username, self.user2.username)

    def save(self, *args, **kwargs):
        '''
        override save function
        check if user1 != user2 
        switch postion if user1.username > user2.username
        '''
        from copy import deepcopy

        if self.user1.username > self.user2.username:
            user3 = deepcopy(self.user1)
            self.user1 = self.user2
            self.user2 = user3
        elif self.user1.username == self.user2.username:
            raise ValidationError('You can not be a friend of yourself')
        else:
            pass

        return super().save(*args, **kwargs)


class FriendRequest(models.Model):
    '''
    link table to track user's friend request
    from_user send friend request to to_user
    '''

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sender')

    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receiver')

    class Meta:
        app_label = 'hyperion'
        unique_together = ('from_user', 'to_user',)

    def __str__(self):
        return super().__str__()+' {} -> {} '.format(
            self.from_user.username, self.to_user.username)

    def save(self, *args, **kwargs):
        '''
        override save function
        check if user1 != user2 
        switch postion if user1.username > user2.username
        '''
        from copy import deepcopy

        if self.from_user.username == self.to_user.username:
            raise ValidationError("You can't send friend request to yourself")
        else:
            pass

        return super().save(*args, **kwargs)
