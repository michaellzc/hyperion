
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    class Meta:
        app_label = 'hyperion'

    author = models.OneToOneField(
            User, 
            on_delete=models.CASCADE,
            related_name='profile')
    displayName = models.CharField(max_length=20)
    website = models.URLField(verbose_name="personal website", blank=True)
    bio = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return super().__str__()+' user: '+str(self.author.pk)

    def get_friends(self):
        from django.contrib.auth.models import User
        query = [row.user1 for row in self.author.friends.all()] +\
                [row.user2 for row in self.author.friends_of.all()] 
        return query

# set signal for auto-create authorProfile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(author=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class UserToUser(models.Model):

    
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
                self.user1.username,self.user2.username)

    def save(self,*args,**kwargs):
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

        return super().save(*args,**kwargs)
