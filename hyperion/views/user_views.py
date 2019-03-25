# pylint: disable=broad-except
from urllib.parse import urlparse

import requests

from django.contrib.auth.models import User, Group

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from hyperion.serializers import UserSerializer, GroupSerializer, UserProfileSerializer
from hyperion.authentication import HyperionBasicAuthentication
from hyperion.models import Server


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@api_view(["GET"])
@authentication_classes((HyperionBasicAuthentication,))
@permission_classes((permissions.IsAuthenticated,))
def get_profile(request, author_id: str):
    is_local = False

    try:
        # check if authenticated user is a server or local user
        request.user.server
    except User.server.RelatedObjectDoesNotExist:  # pylint: disable=no-member
        # local user shoud not have an one-to-one relationship with Server
        is_local = True

    if is_local:
        # handle local user request
        if author_id.isdigit():
            # local user id
            query = User.objects.get(pk=int(author_id))
            user_profile = UserSerializer(query).data
            friends = list(query.profile.get_friends())
            serializer = UserProfileSerializer(
                friends, many=True, context={"fields": ["id", "host", "display_name", "url"]}
            )
            user_profile["friends"] = serializer.data
            return Response(user_profile)
        else:
            # Handle fetching profile for a foreign user
            try:
                parsed_url = urlparse(author_id)
                foreign_server = Server.objects.get(
                    url="{}://{}".format(parsed_url.scheme, parsed_url.netloc)
                )
                response = requests.get(
                    "{}{}".format(foreign_server.endpoint, parsed_url.path),
                    auth=(foreign_server.foreign_db_username, foreign_server.foreign_db_password),
                )
                return Response(response.json())
            except Server.DoesNotExist:
                return Response(
                    {"succcess": False, "message": "Foreign server does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except requests.exceptions.RequestException:
                return Response(
                    {"succcess": False, "message": "Failed to retrieve foreign server profile."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
    else:
        # handle foreign server request
        query = User.objects.get(pk=int(author_id))
        result = UserSerializer(query).data
        return Response(result)


@api_view(["PATCH"])
@authentication_classes((HyperionBasicAuthentication,))
@permission_classes((permissions.IsAuthenticated,))
def update_profile(request):
    body = request.data
    if body.get("query", None) != "updateProfile":
        return Response({"message": "Invalid request."}, status=400)

    new_profile = body.get("author", None)

    try:

        user = User.objects.get(username=request.user)
        user.email = new_profile.get("email", user.email)

        user.profile.bio = new_profile.get("bio", user.profile.bio)
        user.profile.github = new_profile.get("github", user.profile.github)
        user.profile.display_name = new_profile.get("display_name", user.profile.display_name)

        # it will save profile and user
        user.save()

    except Exception as some_error:
        return Response(
            {"query": "updateProfile", "success": False, "message": str(some_error)},
            content_type="application/json",
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {"query": "updateProfile", "success": True, "message": "User profile is updated."},
        content_type="application/json",
        status=status.HTTP_200_OK,
    )
