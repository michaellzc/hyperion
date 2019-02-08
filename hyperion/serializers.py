from django.contrib.auth.models import User, Group
from rest_framework import serializers
from hyperion.models import Comment
from django.conf import settings

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class UserSerializer(serializers.ModelSerializer):

    bio = serializers.CharField(source='profile.bio', allow_blank=True, max_length=100, required=False)
    host = serializers.CharField(source='profile.host.name', max_length=200, required=False)
    display_name = serializers.CharField(source='profile.display_name', max_length=20)
    id = serializers.CharField(source='profile.get_full_id')
    url = serializers.CharField(source='profile.url', max_length=200)
    github = serializers.CharField(source='profile.github', max_length=200, allow_blank=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'bio',
                  'host', 'first_name', 'last_name',
                  'display_name', 'url', 'github')

    # Not sure if this solution effects create/update
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'host' not in data.keys():
            data['host'] = settings.HYPERION_HOSTNAME
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content_type', 'comment',
                  'published', 'author')






