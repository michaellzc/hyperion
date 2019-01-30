
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
        accept_friend_request: delete FriendRequest and create Friend
        decline_friend_request: delete FriendRequest

    '''
    class Meta:
        app_label = 'hyperion'

    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        null=True,
        blank=True
    )
    display_name = models.CharField(max_length=20)
    website = models.URLField(verbose_name="personal website", blank=True)
    bio = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return super().__str__()+' user: '+str(self.author.pk)

    def get_friends(self):
        from hyperion.models import UserProfile
        # return queryset of all author's friends via Friend
        return UserProfile.objects.filter(friends__profile1=self) | \
            UserProfile.objects.filter(friends_of__profile2=self)

    def get_friends_friends(self):
        # get all friends's friends into qs and remove self and friends
        # from qs
        from hyperion.models import UserProfile
        qs = UserProfile.objects.none()
        friends = self.get_friends()
        for f in friends:
            qs = qs | f.get_friends()
        qs = qs.difference(UserProfile.objects.filter(pk=self.pk), friends)
        return qs

    def send_friend_request(self, to_profile):
        # update FriendRequest
        # to_user is User object
        from hyperion.models import FriendRequest
        FriendRequest.objects.create(
            from_profile=self, to_profile=to_profile)
        return

    def accept_friend_request(self, from_profile):
        # if there is a request
        # from_user is User object
        from hyperion.models import Friend
        query = FriendRequest.objects.get(
            from_profile=from_profile, to_profile=self)
        if query:
            Friend.objects.create(profile1=self, profile2=from_profile)
            query.delete()
        return

    def decline_friend_request(self, from_profile):
        # if there is a request, remove it
        query = FriendRequest.objects.get(
            from_profile=from_profile, to_profile=self)
        if query:
            query.delete()
        return


# set signal for auto-create authorProfile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            author=instance, display_name=instance.username)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Friend(models.Model):
    '''
    link table to track user's friends
    '''

    profile1 = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE,
        related_name='friends_of')
    profile2 = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE,
        related_name='friends')

    class Meta:
        app_label = 'hyperion'
        unique_together = ('profile1', 'profile2',)

    def __str__(self):
        return super().__str__()+' {} <-> {} '.format(
            self.profile1.display_name, self.profile2.display_name)

    def save(self, *args, **kwargs):
        '''
        override save function
        check if user1 != profile2 
        switch postion if user1.username > profile2.username
        '''
        from copy import deepcopy

        if self.profile1.id > self.profile2.id:
            profile3 = deepcopy(self.profile1)
            self.profile1 = self.profile2
            self.profile2 = profile3
        elif self.profile1.id == self.profile2.id:
            raise ValidationError('You can not be a friend of yourself')
        else:
            pass

        return super().save(*args, **kwargs)


class FriendRequest(models.Model):
    '''
    link table to track user's friend request
    from_user send friend request to to_user
    '''

    from_profile = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE,
        related_name='sender')

    to_profile = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE,
        related_name='receiver')

    class Meta:
        app_label = 'hyperion'
        unique_together = ('from_profile', 'to_profile',)

    def __str__(self):
        return super().__str__()+' {} -> {} '.format(
            self.from_user.display_name, self.to_profile.display_name)

    def save(self, *args, **kwargs):
        '''
        override save function
        check if profile1 != profile2 
        switch postion if profile1.username > profile2.username
        '''
        from copy import deepcopy

        if self.from_profile.id == self.to_profile.id:
            raise ValidationError("You can't send friend request to yourself")
        else:
            pass

        return super().save(*args, **kwargs)
