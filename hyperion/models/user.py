# pylint: disable=arguments-differ,unused-argument, broad-except, len-as-condition
from urllib.parse import urlparse

from django.db import models
from django.apps import apps
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.conf import settings

from hyperion.errors import FriendAlreadyExist
from hyperion.models.server import Server
from hyperion.utils import ForeignServerHttpUtils


class UserProfile(models.Model):
    """
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

    """

    class Meta:
        app_label = "hyperion"

    author = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", null=True, blank=True
    )
    display_name = models.CharField(max_length=20)
    website = models.URLField(verbose_name="personal website", blank=True)
    bio = models.CharField(max_length=100, blank=True)
    # url can't be blank otherwise foreign user will can not be identified
    url = models.CharField(max_length=200, blank=True)
    github = models.URLField(max_length=200, blank=True)
    host = models.ForeignKey("Server", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.author:
            return super().__str__() + " user: " + str(self.display_name)
        else:
            return super().__str__() + " user(foreign): " + str(self.display_name)

    def get_full_id(self):
        if self.author:
            if self.host is None:
                host_name = settings.HYPERION_HOSTNAME
                return "{}/author/{}".format(host_name, self.author.id)
        return self.url

    def get_url(self):
        return self.get_full_id()

    def get_host(self):
        return self.get_full_id().split("/author/")[0]

    def get_type(self):
        # return UserProfile class either host or foreign
        if self.host and self.author is None:
            return "foreign"
        elif self.author and self.host is None:
            return "host"
        else:
            raise ValidationError("both of user and host are None")

    def get_friends(self, including="all"):
        # return queryset of all author's friends via Friend
        # including can be ['all','host','foreign']
        # from hyperion.models import UserProfile
        apps.get_model("hyperion", "UserProfile")
        query_set = UserProfile.objects.filter(friends__profile1=self) | UserProfile.objects.filter(
            friends_of__profile2=self
        )
        if including == "foreign":
            return query_set.difference(query_set.filter(host=None))
        elif including == "host":
            return query_set.filter(host=None)
        else:
            return query_set

    def get_friends_friends(self):
        # get all friends's friends into qs and remove self and friends
        # from qs
        # from hyperion.models import UserProfile
        apps.get_model("hyperion", "UserProfile")
        query_set = UserProfile.objects.none()
        friends = self.get_friends()
        for friend in friends:
            query_set = query_set | friend.get_friends()
        query_set = query_set.difference(UserProfile.objects.filter(pk=self.pk), friends)
        return query_set

    def send_friend_request(self, to_profile):
        # update FriendRequest
        # to_profile is UserProfile object
        # from hyperion.models import FriendRequest
        apps.get_model("hyperion", "FriendRequest")
        # if self.host:
        #     raise ValidationError(
        #         'Froeign user profile has not send_friend_request'
        #     )
        # ISSUE TODO: only to_profile should be in host
        # if to_profile.host:
        #     raise ValidationError("the one get friend request should be our local author")

        # if they are already friend => raise error
        # https://stackoverflow.com/questions/42206351/django-checking-if-objects-exists-and-raising-error-if-it-does
        qs1 = Friend.objects.filter(profile1=self, profile2=to_profile)
        qs2 = Friend.objects.filter(profile1=to_profile, profile2=self)
        if qs1.exists() or qs2.exists():
            raise FriendAlreadyExist
        else:
            FriendRequest.objects.create(from_profile=self, to_profile=to_profile)

    def accept_friend_request(self, from_profile):
        # if there is a request
        # from_profile is UserProfile object
        # from hyperion.models import Friend
        apps.get_model("hyperion", "Friend")
        if self.host:
            raise ValidationError("Foreign user profile has not accept_friend_request")
        query = FriendRequest.objects.get(from_profile=from_profile, to_profile=self)
        if query:
            Friend.objects.create(profile1=self, profile2=from_profile)
            query.delete()

    def decline_friend_request(self, from_profile):
        # if there is a request, remove it
        if self.host:
            raise ValidationError("Foreign user profile has not decline_friend_request")
        query = FriendRequest.objects.get(from_profile=from_profile, to_profile=self)
        if query:
            query.delete()

    def check_remote_foaf_relationship(self, remote_user_full_id):
        try:
            # find the server first
            remote_user_host_name = "{uri.scheme}://{uri.netloc}".format(
                uri=urlparse(remote_user_full_id)
            )
            foreign_server = Server.objects.get(url=remote_user_host_name)
            remote_user_id = remote_user_full_id.split("/author/")[-1]

            # fetch friendlist
            resp = ForeignServerHttpUtils.get(
                foreign_server, "/author/" + remote_user_id + "/friends"
            )
            if resp.status_code != 200:
                raise Exception("failed getting the friend_list")
            remote_user_friend_list = resp.json()["authors"]
            # remote_user_friend_list = [friend["id"] for friend in resp.json()["authors"]]
            # print(remote_user_friend_list)

            own_friend_list = list(self.get_friends().values_list("url", flat=True))
            intersection_friends = list(set(remote_user_friend_list) & set(own_friend_list))

            return len(intersection_friends) > 0

        except Exception as some_error:
            # print(remote_user_full_id)
            # print(remote_user_host_name)
            print(some_error, "error in check_remote_foaf_relationship")
            return False

    def save(self, *args, **kwargs):
        """
        override save function
        """
        if self.host and self.author:
            raise ValidationError("Foreign UserProfile can't have author")
        elif self.host is None and self.author is None:
            raise ValidationError("UserProfile must have author")
        else:
            return super().save(*args, **kwargs)


# set signal for auto-create authorProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(author=instance, display_name=instance.username)
        user_profile.url = user_profile.get_full_id()
        user_profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Friend(models.Model):
    """
    link table to track user's friends
    """

    profile1 = models.ForeignKey("UserProfile", on_delete=models.CASCADE, related_name="friends_of")
    profile2 = models.ForeignKey("UserProfile", on_delete=models.CASCADE, related_name="friends")

    class Meta:
        app_label = "hyperion"
        unique_together = ("profile1", "profile2")

    def __str__(self):
        return super().__str__() + " {} <-> {} ".format(
            self.profile1.display_name, self.profile2.display_name
        )

    def save(self, *args, **kwargs):
        """
        override save function
        check if user1 != profile2
        switch postion if user1.username > profile2.username
        """
        from copy import deepcopy

        if self.profile1.get_type() == "foreign" and self.profile2.get_type() == "foreign":
            raise ValidationError("You cannot set two foreign user as friend")

        if self.profile1.id > self.profile2.id:
            profile3 = deepcopy(self.profile1)
            self.profile1 = self.profile2
            self.profile2 = profile3
        elif self.profile1.id == self.profile2.id:
            raise ValidationError("You can not be a friend of yourself")
        else:
            pass

        return super().save(*args, **kwargs)


class FriendRequest(models.Model):
    """
    link table to track user's friend request
    from_profile send friend request to to_profile
    """

    from_profile = models.ForeignKey("UserProfile", on_delete=models.CASCADE, related_name="sender")

    to_profile = models.ForeignKey("UserProfile", on_delete=models.CASCADE, related_name="receiver")

    class Meta:
        app_label = "hyperion"
        unique_together = ("from_profile", "to_profile")

    def __str__(self):
        return super().__str__() + " {} -> {} ".format(
            self.from_profile.display_name, self.to_profile.display_name
        )

    def save(self, *args, **kwargs):
        """
        override save function
        check if profile1 != profile2
        switch postion if profile1.username > profile2.username
        """
        if self.from_profile.id == self.to_profile.id:
            raise ValidationError("You can't send friend request to yourself")
        else:
            pass

        return super().save(*args, **kwargs)
