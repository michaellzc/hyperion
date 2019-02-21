from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from hyperion.serializers import UserProfileSerializer

import json


def _get_error_response(query_name, is_success, message):
    content = {"query": query_name,
               "success": is_success,
               "message": message}
    return json.dumps(content)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,)) #??
def friend_list(request, author_id):
    if not request.user.is_authenticated:
        return Response(_get_error_response("friends", False, "Not login"),
                        status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        # get all friends to this authenticated author
        friends = list(request.user.profile.get_friends())
        # https://stackoverflow.com/questions/47119879/how-to-get-specific-field-from-serializer-of-django-rest-framework
        serializer = UserProfileSerializer(friends,
                                           many=True,
                                           context={'fields': ['id', "host", "display_name", "url"]})
        content = {"query": "friends", "count": len(friends), "author": serializer.data}
        return Response(json.dumps(content), content_type='application/json', status=status.HTTP_200_OK)

    # elif request.method == "POST":
    #     pass



