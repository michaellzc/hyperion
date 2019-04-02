from django.contrib.auth.models import User, Group
from django.conf import settings
from rest_framework import serializers
from rest_framework.fields import ListField

from hyperion.models import *

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ("url", "name")


class UserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(
        source="profile.bio", allow_blank=True, max_length=100, required=False
    )
    host = serializers.CharField(source="profile.host.name", max_length=200, required=False)
    display_name = serializers.CharField(source="profile.display_name", max_length=20)
    id = serializers.CharField(source="profile.get_full_id")
    url = serializers.CharField(source="profile.get_url")
    github = serializers.CharField(
        source="profile.github", max_length=200, allow_blank=True, required=False
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "bio",
            "host",
            "first_name",
            "last_name",
            "display_name",
            "url",
            "github",
            "is_active",
        )

    # Not sure if this solution effects create/update
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if "host" not in data.keys():
            data["host"] = settings.HYPERION_HOSTNAME
        return data


class UserSignUpSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_create = User.objects.create(
            username=validated_data["username"], email=validated_data["email"]
        )
        user_create.set_password(validated_data["password"])
        user_create.is_active = False
        user_create.save()

        return user_create

    class Meta:
        model = User
        fields = ("username", "email", "password")


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        source="get_full_id", allow_blank=True, max_length=100, required=False
    )
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    email = serializers.CharField(
        source="author.email", allow_blank=True, max_length=100, required=False
    )
    username = serializers.CharField(
        source="author.username", allow_blank=True, max_length=100, required=False
    )
    first_name = serializers.CharField(
        source="author.first_name", allow_blank=True, max_length=100, required=False
    )
    last_name = serializers.CharField(
        source="author.last_name", allow_blank=True, max_length=100, required=False
    )
    host = serializers.CharField(
        source="get_host", allow_blank=True, max_length=100, required=False
    )
    url = serializers.CharField(source="get_full_id", read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "email",
            "bio",
            "author",
            "host",
            "first_name",
            "last_name",
            "display_name",
            "url",
            "github",
            "username",
        )

    # Not sure if this solution effects create/update
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if "host" not in data.keys():
            data["host"] = settings.HYPERION_HOSTNAME
        return data

    # https://stackoverflow.com/questions/47119879/how-to-get-specific-field-from-serializer-of-django-rest-framework
    # https://github.com/encode/django-rest-framework/blob/master/rest_framework/serializers.py
    def get_field_names(self, declared_fields, info):
        field_names = self.context.get("fields", None)
        if field_names:
            return field_names

        return super(UserProfileSerializer, self).get_field_names(declared_fields, info)


class CommentSerializer(serializers.ModelSerializer):
    # author = UserProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "content_type", "comment", "published", "author", "post")
        extra_kwargs = {"post": {"write_only": True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        serializer = UserProfileSerializer(instance.author)
        data["author"] = serializer.data
        return data


class PostSerializer(serializers.ModelSerializer):
    """
    comments: read_only
    visible_to: required in serializer, not required in deserializer
    """

    author = UserProfileSerializer(read_only=True)
    comments = CommentSerializer(source="get_comments", many=True, read_only=True)
    visible_to = serializers.ListField(child=serializers.CharField())
    source = serializers.CharField(source="get_source", max_length=200, required=False)
    origin = serializers.CharField(source="get_source", max_length=200, required=False)

    class Meta:
        model = Post
        fields = "__all__"

    # def to_internal_value(self, data):
    #     visible_to = data.pop("visible_to", [])
    #     data = super().to_internal_value(data)
    #     data["visible_to"] = visible_to
    #     return data

    def create(self, validated_data):
        # https://stackoverflow.com/questions/30203652/how-to-get-request-user-in-django-rest-framework-serializer
        # if there are some visible_to user profiel
        user = self.context["request"].user
        visible_to_data = validated_data.pop("visible_to", [])
        post = Post.objects.create(author=user.profile, **validated_data)
        visible_to = [
            User.objects.get(username=username).profile.url for username in visible_to_data
        ]
        post.visible_to = visible_to
        post.save()
        return post

    def update(self, instance, validated_data):
        visible_to_data = validated_data.pop("visible_to", [])
        post = super().update(instance, validated_data)
        visible_to = [
            User.objects.get(username=username).profile.url for username in visible_to_data
        ]
        post.visible_to = visible_to
        return post


class FriendRequestSerializer(serializers.ModelSerializer):
    # https://stackoverflow.com/questions/30560470/context-in-nested-serializers-django-rest-framework
    author = serializers.SerializerMethodField("get_author_profile_serializer")
    friend = serializers.SerializerMethodField("get_friend_profile_serializer")

    class Meta:
        model = FriendRequest
        fields = ("id", "author", "friend")

    def get_author_profile_serializer(self, obj):
        user_fields = self.context["user_fields"]
        serializer = UserProfileSerializer(
            obj.from_profile, read_only=True, context={"fields": user_fields}
        )
        return serializer.data

    def get_friend_profile_serializer(self, obj):
        user_fields = self.context["user_fields"]
        serializer = UserProfileSerializer(
            obj.to_profile, read_only=True, context={"fields": user_fields}
        )
        return serializer.data
        