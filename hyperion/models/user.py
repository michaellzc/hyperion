
from django.db import models
from django.apps import apps
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
        host: if not None, this UserProfile' author is from other server
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
    host = models.ForeignKey(
        'Server',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        if self.author:
            return super().__str__()+' user: '+str(self.display_name)
        else:
            return super().__str__()+'foreign_user'+str(self.display_name)

    def get_type(self):
        # return UserProfile class either host or foreign
        if self.host and self.author is None:
            return 'foreign'
        elif self.author and self.host is None:
            return 'host'
        else:
            raise ValidationError('both of user and host are None')

    def get_friends(self, including='all'):
        # return queryset of all author's friends via Friend
        # including can be ['all','host','foreign']
        # from hyperion.models import UserProfile
        apps.get_model('hyperion', 'UserProfile')
        query_set = UserProfile.objects.filter(friends__profile1=self) | \
            UserProfile.objects.filter(friends_of__profile2=self)
        if including == 'foreign':
            return query_set.difference(query_set.filter(host=None))
        elif including == 'host':
            return query_set.filter(host=None)
        else:
            return query_set

    def get_friends_friends(self):
        # get all friends's friends into qs and remove self and friends
        # from qs
        # from hyperion.models import UserProfile
        apps.get_model('hyperion', 'UserProfile')
        query_set = UserProfile.objects.none()
        friends = self.get_friends()
        for friend in friends:
            query_set = query_set | friend.get_friends()
        query_set = query_set.difference(
            UserProfile.objects.filter(pk=self.pk), friends
        )
        return query_set

    def send_friend_request(self, to_profile):
        # update FriendRequest
        # to_profile is UserProfile object
        # from hyperion.models import FriendRequest
        apps.get_model('hyperion', 'FriendRequest')
        if self.host:
            raise ValidationError(
                'Froeign user profile has not send_friend_request'
            )
        FriendRequest.objects.create(
            from_profile=self, to_profile=to_profile)

    def accept_friend_request(self, from_profile):
        # if there is a request
        # from_profile is UserProfile object
        # from hyperion.models import Friend
        apps.get_model('hyperion', 'Friend')
        if self.host:
            raise ValidationError(
                'Froeign user profile has not accept_friend_request'
            )
        query = FriendRequest.objects.get(
            from_profile=from_profile, to_profile=self)
        if query:
            Friend.objects.create(profile1=self, profile2=from_profile)
            query.delete()

    def decline_friend_request(self, from_profile):
        # if there is a request, remove it
        if self.host:
            raise ValidationError(
                'Froeign user profile has not decline_friend_request'
            )
        query = FriendRequest.objects.get(
            from_profile=from_profile, to_profile=self)
        if query:
            query.delete()

    def save(self, *args, **kwargs):
        '''
        override save function
        '''
        if self.host and self.author:
            raise ValidationError("Foreign UserProfile can't have author")
        elif self.host is None and self.author is None:
            raise ValidationError('UserProfile must have author')
        else:
            return super().save(*args, **kwargs)

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
        if self.profile1.get_type() == 'foreign' and \
                self.profile2.get_type() == 'foreign':
            raise ValidationError(
                'You cannot set two foreign user as friend'
            )

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
    from_profile send friend request to to_profile
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
            self.from_profile.display_name, self.to_profile.display_name)

    def save(self, *args, **kwargs):
        '''
        override save function
        check if profile1 != profile2
        switch postion if profile1.username > profile2.username
        '''
        if self.from_profile.id == self.to_profile.id:
            raise ValidationError("You can't send friend request to yourself")
        else:
            pass

        return super().save(*args, **kwargs)
