# pylint: disable=broad-except, too-many-branches, too-many-statements
import json
from urllib.parse import urlparse

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from django.conf import settings

from hyperion.serializers import UserProfileSerializer, FriendRequestSerializer
from hyperion.models import UserProfile, FriendRequest, Friend, Server
from hyperion.authentication import HyperionBasicAuthentication
from hyperion.errors import FriendAlreadyExist
from hyperion.utils import ForeignServerHttpUtils


def _get_error_response(query_name, is_success, message):
    content = {"query": query_name, "success": is_success, "message": message}
    return content


@api_view(["GET", "POST"])
@authentication_classes((HyperionBasicAuthentication,))
@permission_classes((permissions.IsAuthenticated, permissions.AllowAny))
# don't know how to vendor error message to default error raise
def friend_list(request, author_id):

    if request.method == "GET":
        author_profile = User.objects.get(id=author_id).profile
        # get all friends to this authenticated author
        friends = list(author_profile.get_friends())
        # https://stackoverflow.com/questions/47119879/how-to-get-specific-field-from-serializer-of-django-rest-framework
        serializer = UserProfileSerializer(
            friends, many=True, context={"fields": ["id", "host", "display_name", "url"]}
        )
        content = {"query": "friends", "count": len(friends), "author": serializer.data}
        return Response(content, content_type="application/json", status=status.HTTP_200_OK)

    elif request.method == "POST":
        try:
            body_unicode = request.body.decode("utf-8")
            body = json.loads(body_unicode)

            if body["query"] != "friends":
                raise Exception("query should be friends")

            # author = User.objects.get(pk=int(body["author"]))
            author_profile = UserProfile.objects.get(url=body["author"])

            # get friend url with author
            author_friend_list = list(author_profile.get_friends().values_list("url", flat=True))
            pending_friend_list = body["authors"]
            # https://stackoverflow.com/questions/3697432/how-to-find-list-intersection/33067553

            result_friend_list = list(set(author_friend_list) & set(pending_friend_list))
            # print(result_friend_list)

            content = {"query": "friends", "author": body["author"], "authors": result_friend_list}
            return Response(content, content_type="application/json", status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                _get_error_response("friends", False, "the author is not exist"),
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as some_error:
            return Response(
                _get_error_response("friends", False, str(some_error)),
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["GET"])
@authentication_classes((HyperionBasicAuthentication,))
@permission_classes((permissions.IsAuthenticated, permissions.AllowAny))
def check_friendship(request, author_id_1, service2, author_id_2):
    # print("author1 ", author_id_1)
    # TO DO maybe http
    author2 = "https://" + service2 + "/author/" + author_id_2
    # print("author2 ", author2)

    try:
        # get author1
        author1 = User.objects.get(pk=int(author_id_1))

        # get friend url with author1
        author1_friend_list = list(author1.profile.get_friends().values_list("url", flat=True))
        # print(author1_friend_list)
        content = {"query": "friends", "authors": [author1.profile.get_full_id(), author2]}

        if author2 in author1_friend_list:
            content["friends"] = True
        else:
            content["friends"] = False

        return Response(content, content_type="application/json", status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response(
            _get_error_response("friends", False, "the author 1 is not exist"),
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as some_error:
        return Response(
            _get_error_response("friends", False, str(some_error)),
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET", "POST"])
@authentication_classes((HyperionBasicAuthentication,))
@permission_classes((permissions.IsAuthenticated, permissions.AllowAny))
def friend_request(request):

    if request.method == "GET":
        # get all friend request which to_friend would be request.user
        friend_request_list = FriendRequest.objects.filter(to_profile=request.user.profile)

        content = {
            "query": "friendrequests",
            "frinedrequests": FriendRequestSerializer(
                friend_request_list,
                many=True,
                context={"user_fields": ["id", "host", "display_name", "url"]},
            ).data,
        }

        return Response(content, content_type="application/json", status=status.HTTP_200_OK)

    elif request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            if body["query"] != "friendrequest":
                raise Exception("query should be friendrequest")

            # get the host from url to compare with host attribute
            # https://stackoverflow.com/questions/9626535/get-protocol-host-name-from-url
            # host_name = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(body["author"]["id"]))
            #
            # if host_name != body["author"]["host"]:
            #     raise Exception("we can't save the profile which host != url.host")

            friend_host_name = "{uri.scheme}://{uri.netloc}".format(
                uri=urlparse(body["friend"]["id"])
            )

            # check if the request user is local or remote
            is_local = False
            try:
                server = request.user.server
            except User.server.RelatedObjectDoesNotExist:  # pylint: disable=no-member
                is_local = True

            if is_local:  # if author is local
                # get the author profile
                author_profile = User.objects.get(
                    pk=int(body["author"]["id"].split("/")[-1])
                ).profile
                # check if the to_friend is local or remote
                if friend_host_name == settings.HYPERION_HOSTNAME:  # friend is local
                    friend_profile = User.objects.get(
                        pk=int(body["friend"]["id"].split("/")[-1])
                    ).profile
                else:  # friend is remote
                    # check if the friend profile exists
                    try:
                        friend_profile = UserProfile.objects.get(url=body["friend"]["id"])
                    except UserProfile.DoesNotExist:
                        remote_server_user = User.objects.get(profile__url=friend_host_name)
                        friend_profile = UserProfile.objects.create(
                            # TO DO what's the default value of display_name
                            display_name=body["friend"].get("displayName", ""),
                            host=remote_server_user.server,
                            url=body["friend"]["id"],
                        )

                    # send friend request to remote server
                    friend_request_body = {
                        "query": "friendrequest",
                        "author": UserProfileSerializer(
                            author_profile,
                            context={"fields": ["id", "host", "display_name", "url"]},
                        ).data,
                        "friend": UserProfileSerializer(
                            friend_profile,
                            context={"fields": ["id", "host", "display_name", "url"]},
                        ).data,
                    }
                    foreign_server = Server.objects.get(url=friend_host_name)
                    resp = ForeignServerHttpUtils.post(
                        foreign_server, "/friendrequest", json=friend_request_body
                    )
                    if resp.status_code != 200:
                        raise Exception(
                            "send friendrequest to remote server failed, reason={}".format(
                                resp.content
                            )
                        )

            else:  # if author is remote
                # check if the author profile exists
                try:
                    author_profile = UserProfile.objects.get(url=body["author"]["id"])
                except UserProfile.DoesNotExist:
                    author_profile = UserProfile.objects.create(
                        display_name=body["author"].get("displayName", ""),
                        host=server,
                        url=body["author"]["id"],
                    )
                # friend must be local
                friend_profile = User.objects.get(
                    pk=int(body["friend"]["id"].split("/")[-1])
                ).profile

            # if there are already friend => return 204
            try:
                author_profile.send_friend_request(friend_profile)
            except FriendAlreadyExist:
                return Response(status=status.HTTP_204_NO_CONTENT)

            # check if already get reverse edition friend request
            reverse_friend_request = FriendRequest.objects.filter(
                from_profile=friend_profile, to_profile=author_profile
            )
            if reverse_friend_request.exists():
                Friend.objects.create(profile1=author_profile, profile2=friend_profile)
                FriendRequest.objects.filter(
                    from_profile=author_profile, to_profile=friend_profile
                ).delete()
                FriendRequest.objects.filter(
                    from_profile=friend_profile, to_profile=author_profile
                ).delete()

                return Response(
                    {
                        "query": "friendrequest",
                        "success": True,
                        "message": "Two way friendrequests create friendship",
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"query": "friendrequest", "success": True, "message": "friendrequest sent"},
                status=status.HTTP_200_OK,
            )

        except Exception as some_error:
            # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            # message = template.format(type(some_error).__name__, some_error.args)
            # print(message)
            return Response(
                _get_error_response("friendrequest", False, str(some_error)),
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["PUT"])
@authentication_classes((HyperionBasicAuthentication,))
@permission_classes((permissions.IsAuthenticated, permissions.AllowAny))
def action_friend_request(request, friendrequest_id):
    try:
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)

        # get the friend request first
        friend_request_obj = FriendRequest.objects.get(pk=friendrequest_id)

        # check if the request user is the user being friend
        if request.user.id != friend_request_obj.to_profile.author.id:
            raise Exception(
                "the request user doesn't have permission to do action in this friend request"
            )

        if body["query"] != "friendrequestAction":
            raise Exception("query should be friendrequestAction")

        # check the accepted information
        if body["accepted"]:
            # if the friend request author is remote user
            parsed_friend_uri = urlparse(friend_request_obj.from_profile.url)
            author_host_name = "{uri.scheme}://{uri.netloc}".format(uri=parsed_friend_uri)
            # print("asfsdf", author_host_name)
            if author_host_name != settings.HYPERION_HOSTNAME:
                # send friendrequest(reverse edition)
                friend_request_reverse_body = {
                    "query": "friendrequest",
                    "author": UserProfileSerializer(
                        friend_request_obj.to_profile,
                        context={"fields": ["id", "host", "display_name", "url"]},
                    ).data,
                    "friend": UserProfileSerializer(
                        friend_request_obj.from_profile,
                        context={"fields": ["id", "host", "display_name", "url"]},
                    ).data,
                }
                # print(friend_request_reverse_body["friend"]["host"])
                foreign_server = Server.objects.get(
                    url=friend_request_reverse_body["friend"]["host"]
                )
                resp = ForeignServerHttpUtils.post(
                    foreign_server, "/friendrequest", json=friend_request_reverse_body
                )
                if resp.status_code != 200:
                    raise Exception(
                        "send back friendrequest to remote server failed, reason={}".format(
                            resp.content
                        )
                    )

            friend_request_obj.to_profile.accept_friend_request(friend_request_obj.from_profile)
            msg = "accept the friend request"
            accepted = True
        else:
            friend_request_obj.to_profile.decline_friend_request(friend_request_obj.from_profile)
            msg = "decline the friend request"
            accepted = False

        serializer = FriendRequestSerializer(
            friend_request_obj, context={"user_fields": ["id", "host", "display_name", "url"]}
        )
        content = {
            "query": "friendrequestAction",
            "friendrequest": serializer.data,
            "accepted": accepted,
            "success": True,
            "message": msg,
        }
        return Response(content, status=status.HTTP_200_OK)

    except FriendRequest.DoesNotExist:
        return Response(
            _get_error_response("friendrequestAction", False, "friend request is not exist"),
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as some_error:
        return Response(
            _get_error_response("friendrequestAction", False, str(some_error)),
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@authentication_classes((HyperionBasicAuthentication,))
@permission_classes((permissions.IsAuthenticated, permissions.AllowAny))
def unfollow_request(request):
    # so far only local user can do unfriend action
    try:
        body = json.loads(request.body.decode("utf-8"))

        if body["query"] != "unfollow":
            raise Exception("query should be unfollow")

        # get the host from url to compare with host attribute
        # https://stackoverflow.com/questions/9626535/get-protocol-host-name-from-url
        # host_name = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(body["author"]["id"]))
        # if host_name != body["author"]["host"]:
        #     raise Exception("we can't save the profile which host != url.host")

        friend_host_name = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(body["friend"]["id"]))

        is_local = False
        try:
            _ = request.user.server
        except User.server.RelatedObjectDoesNotExist:  # pylint: disable=no-member
            is_local = True

        if is_local:  # the request user is local
            author_id = int(body["author"]["id"].split("/")[-1])
            if request.user.id != author_id:
                raise Exception("request user is not the author")
            author_profile = User.objects.get(pk=author_id).profile

            # check if the friend is local or remote
            if friend_host_name == settings.HYPERION_HOSTNAME:  # friend is local
                friend_profile = User.objects.get(
                    pk=int(body["friend"]["id"].split("/")[-1])
                ).profile
            else:  # friend is remote
                friend_profile = UserProfile.objects.get(url=body["friend"]["id"])

                # send unfollow request to remote server
                unfollow_body = {
                    "query": "unfollow",
                    "author": UserProfileSerializer(
                        author_profile, context={"fields": ["id", "host", "display_name", "url"]}
                    ).data,
                    "friend": UserProfileSerializer(
                        friend_profile, context={"fields": ["id", "host", "display_name", "url"]}
                    ).data,
                }
                foreign_server = Server.objects.get(url=friend_host_name)
                resp = ForeignServerHttpUtils.post(foreign_server, "/unfollow", json=unfollow_body)
                if resp.status_code != 200:
                    raise Exception(
                        "send unfollow to remote server failed, reason={}".format(resp.content)
                    )
        else:  # if the author is remote
            author_profile = UserProfile.objects.get(url=body["author"]["id"])
            friend_profile = User.objects.get(pk=int(body["friend"]["id"].split("/")[-1])).profile

        # if not is_local:
        #     raise Exception("so far, only can handle local user request")

        # # check if the unfriend person exist on our server
        # friend_url = body["friend"]["id"]
        # friend_profile = UserProfile.objects.get(url=friend_url)
        #
        # # check and get author profile
        # author_url = body["author"]["id"]
        # author_profile = UserProfile.objects.get(url=author_url)
        #

        # check if the request user does friend with aim person
        qs1 = Friend.objects.filter(profile1=friend_profile, profile2=author_profile)
        qs2 = Friend.objects.filter(profile1=author_profile, profile2=friend_profile)
        if (not qs1.exists()) and (not qs2.exists()):
            raise Exception("they are not friend")
        else:
            qs1.delete()
            qs2.delete()

        content = {"query": "unfollow", "success": True, "message": "unfollow succeed"}
        return Response(content, status=status.HTTP_200_OK)

    except Exception as some_error:
        return Response(
            _get_error_response("unfollow", False, str(some_error)),
            status=status.HTTP_400_BAD_REQUEST,
        )
