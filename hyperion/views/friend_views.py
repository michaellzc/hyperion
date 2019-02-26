from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from hyperion.serializers import UserProfileSerializer,FriendRequestSerializer
from django.contrib.auth.models import User
from hyperion.models import UserProfile, Server, FriendRequest
from django.conf import settings

import json
from urllib.parse import urlparse
import copy


def _get_error_response(query_name, is_success, message):
    content = {"query": query_name,
               "success": is_success,
               "message": message}
    return json.dumps(content)


# TODO: only handle url request from the server we trust

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated,))
# don't know how to vendor error message to default error raise
def friend_list(request, author_id):

    if request.method == "GET":
        # only GET method needs authorized ??
        if not request.user.is_authenticated:
            return Response(_get_error_response("friends", False, "Not login"),
                            status=status.HTTP_401_UNAUTHORIZED)

        # get all friends to this authenticated author
        friends = list(request.user.profile.get_friends())
        # https://stackoverflow.com/questions/47119879/how-to-get-specific-field-from-serializer-of-django-rest-framework
        serializer = UserProfileSerializer(friends,
                                           many=True,
                                           context={'fields': ['id', "host", "display_name", "url"]})
        content = {"query": "friends", "count": len(friends), "author": serializer.data}
        return Response(json.dumps(content), content_type='application/json', status=status.HTTP_200_OK)

    elif request.method == "POST":
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            if body['query'] == "friends":
                author = User.objects.get(pk=int(body['author']))

                # get friend url with author
                author_friend_list = list(author.profile.get_friends().values_list('url', flat=True),)
                pending_friend_list = body['authors']
                # https://stackoverflow.com/questions/3697432/how-to-find-list-intersection/33067553

                result_friend_list = list(set(author_friend_list) & set(pending_friend_list))
                # print(result_friend_list)

                content = {"query": "friends", "author": body['author'], "authors": result_friend_list}
                return Response(json.dumps(content), content_type='application/json', status=status.HTTP_200_OK)

            else:
                raise Exception("query should be friends")

        except Exception as e:
            return Response(_get_error_response("friends", False, str(e)),
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def check_friendship(request, author_id_1, service2, author_id_2):
    # print("author1 ", author_id_1)
    author2 = "https://" + service2 + "/author/" + author_id_2
    # print("author2 ", author2)

    try:
        # get author1
        author1 = User.objects.get(pk=int(author_id_1))

        # get friend url with author1
        author1_friend_list = list(author1.profile.get_friends().values_list('url', flat=True),)
        # print(author1_friend_list)
        content = {
            "query": "friends",
            "authors": [
                author1.profile.get_full_id(),
                author2,
            ]
        }

        if author2 in author1_friend_list:
            content["friends"] = True
        else:
            content["friends"] = False

        return Response(json.dumps(content), content_type='application/json', status=status.HTTP_200_OK)

    except Exception as e:
        print(str(e))
        return Response(_get_error_response("friends", False, str(e)),
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny, ))
def friend_request(request):

    if request.method == 'GET':
        if not request.user.is_authenticated:
            return Response(_get_error_response("friendrequest", False, "Not login"),
                            status=status.HTTP_401_UNAUTHORIZED)

        # get all friend request which to_friend would be request.user
        friend_request_list = FriendRequest.objects.filter(to_profile=request.user.profile)

        content = {
            "query": "friendrequests",
            'frinedrequests': FriendRequestSerializer(friend_request_list,
                                                      many=True,
                                                      context={
                                                          'user_fields': ['id', "host", "display_name", "url"]
                                                      }).data
        }

        return Response(json.dumps(content), content_type='application/json', status=status.HTTP_200_OK)

    elif request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            if body['query'] == "friendrequest":
                # print(body)

                # check if the to_friend is local author
                friend_id = int(body['friend']['id'].split("/")[-1])

                # get to_friend profile
                to_friend = User.objects.get(pk=friend_id)

                # check if author is in our local host
                if body['author']['host'] == settings.HYPERION_HOSTNAME:
                    author_id = int(body['author']['id'].split("/")[-1])
                    author = User.objects.get(pk=author_id)

                    # send request
                    author.profile.send_friend_request(to_friend.profile)
                else:
                    # check if the author's host is trusted by us
                    try:
                        server = Server.objects.get(name=body['author']['host'])
                    except Server.DoesNotExist:
                        raise Exception("the author's server is not verified by us")

                    # check if we already have this remote user profile
                    try:
                        author_profile = UserProfile.objects.get(url=body['author']['url'])
                        has_author_profile = True
                    except UserProfile.DoesNotExist:
                        # if we doesn't have this user profile
                        # (may also check if user exist in remote server
                        has_author_profile = False

                    if not has_author_profile:
                        # https://stackoverflow.com/questions/9626535/get-protocol-host-name-from-url
                        parsed_uri = urlparse(body['author']['url'])
                        host_name = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
                        if host_name != body['author']['host']:
                            raise Exception("we cant save the profile which host != url.host")

                        try:
                            author_profile = UserProfile.objects.create(
                                display_name=body['author']['display_name'],
                                host=server,
                                url=body['author']['url']
                            )
                        except Exception as e:
                            raise Exception("create author profile failed, reason: " + str(e))

                    author_profile.send_friend_request(to_friend.profile)

                content = {
                    "query": "friendrequest",
                    "success": True,
                    "message": "friendrequest sent"
                }
                return Response(json.dumps(content), status=status.HTTP_200_OK)

            else:
                raise Exception("query should be friendrequest")

        except Exception as e:
            return Response(_get_error_response("friendrequest", False, str(e)),
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def action_friend_request(request, friendrequest_id):
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        # get the friend request first
        friend_request_obj = FriendRequest.objects.get(pk=friendrequest_id)

        # check the accepted information
        if body['accepted']:
            friend_request_obj.to_profile.accept_friend_request(friend_request_obj.from_profile)
            msg = "accept the friend request"
            accepted = True
        else:
            friend_request_obj.to_profile.decline_friend_request(friend_request_obj.from_profile)
            msg = "decline the friend request"
            accepted = False

        serializer = FriendRequestSerializer(friend_request_obj,
                                             context={'user_fields': ['id', "host", "display_name", "url"]})
        content = {
            "query": "friendrequestAction",
            "friendrequest": serializer.data,
            "accepted": accepted,
            "success": True,
            "message": msg
        }
        return Response(json.dumps(content), status=status.HTTP_200_OK)

    except Exception as e:
        return Response(_get_error_response("friendrequestAction", False, str(e)),
                        status=status.HTTP_400_BAD_REQUEST)



