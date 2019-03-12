from django.contrib.auth.models import User, Group
from django.db import IntegrityError

from rest_framework import viewsets, permissions
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response

from hyperion.serializers import UserSerializer, GroupSerializer
from hyperion.authentication import HyperionBasicAuthentication
from hyperion.models import UserProfile


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


@api_view(["PATCH"])
@authentication_classes((HyperionBasicAuthentication,))
@permission_classes((permissions.IsAuthenticated,))
def update_profile(request):
    body = request.data
    if body.get("query", None) != "updateProfile":
        return Response({"message": "Invalid request."}, status=400)

    new_profile = body.get("author", None)

    try:
        current_profile = UserProfile.objects.get(author=request.user)
        current_profile.bio = new_profile.get("bio", current_profile.bio)
        current_profile.github = new_profile.get("github", current_profile.github)
        current_profile.display_name = new_profile.get(
            "display_name", current_profile.display_name
        )
        current_profile.save()

        user = User.objects.get(username=request.user)
        user.first_name = new_profile.get("first_name", user.first_name)
        user.last_name = new_profile.get("last_name", user.last_name)
        user.username = new_profile.get("username", user.username)
        user.save()
    except IntegrityError:
        return Response(
            {
                "query": "updateProfile",
                "success": False,
                "message": "Username is taken.",
            },
            status=422,
        )

    return Response(
        {
            "query": "updateProfile",
            "success": True,
            "message": "User profile is updated.",
        }
    )
