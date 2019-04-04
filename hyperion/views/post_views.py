# pylint: disable=arguments-differ,invalid-name, broad-except, len-as-condition
import json
from urllib.parse import urlparse
import logging
import requests

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status

from hyperion.authentication import HyperionBasicAuthentication
from hyperion.serializers import PostSerializer
from hyperion.models import Post, UserProfile, Server
from hyperion.utils import ForeignServerHttpUtils

logger = logging.getLogger(__name__)


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Post.objects.filter(unlisted=False)
    serializer_class = PostSerializer
    authentication_classes = (HyperionBasicAuthentication,)
    permission_classes = (IsAuthenticated, AllowAny)

    @action(detail=True, methods=["POST"], name="post_auth_posts")
    def post_auth_posts(self, request):
        """
        POST /author/posts
        """
        body = request.data
        post_query = body.get("query", None)
        post_data = body.get("post", None)
        if post_query == "createPost" and post_data:
            post_data["visible_to"] = post_data.get("visible_to", [])
            serializer = PostSerializer(data=post_data, context={"request": request})
            serializer.is_valid()
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"query": "createPost", "success": True, "message": "Author Post Created"}
                )
            else:
                return Response(
                    {"query": "createPost", "success": False, "message": serializer.errors}
                )

    def list(self, request):
        """
        GET /posts
        """
        is_local = False

        try:
            # check if authenticated user is a server or local user
            request.user.server
        except User.server.RelatedObjectDoesNotExist:  # pylint: disable=no-member
            # local user shoud not have an one-to-one relationship with Server
            is_local = True

        posts = self.queryset.filter(visibility="PUBLIC")
        serializer = PostSerializer(posts, many=True)
        data = serializer.data

        foreign_public_posts = []
        if is_local:
            # handle local user request
            # also include foreign public posts
            for server in Server.objects.all():
                try:
                    posts_response = ForeignServerHttpUtils.get(server, "/posts")
                    foreign_public_posts += posts_response.json().get("posts", [])
                except requests.exceptions.RequestException as exception:
                    print(exception)
        else:
            pass
        data += foreign_public_posts
        return Response({"query": "posts", "count": len(data), "posts": data}, status=200)

    # pylint: disable=too-many-locals
    @action(detail=True, methods=["GET"], name="get_auth_posts")
    def get_auth_posts(self, request):
        """
        GET /author/posts
        """
        # check if local user
        foreign_posts = []
        result = []
        try:
            request.user.server
        except User.server.RelatedObjectDoesNotExist:  # pylint: disable=no-member
            # local user
            result = list(
                self.queryset.filter(
                    Q(visibility="PUBLIC")
                    | Q(author=request.user.profile)
                    | Q(visibility="SERVERONLY")
                )
            ) + Post.not_own_posts_visible_to_me(request.user.profile)
            for server in Server.objects.all():
                local_url = request.user.profile.get_url()
                headers = {"X-Request-User-ID": str(local_url)}
                try:
                    response = ForeignServerHttpUtils.get(
                        server, "/author/posts", headers=headers, timeout=5
                    )
                    if response.status_code == 200:
                        body = response.json()
                        if isinstance(body, dict):
                            posts = body.get("posts", [])
                            foreign_posts += posts
                        else:
                            print(server.url)
                except requests.exceptions.RequestException:
                    print(server.url, "Foreign server fucked up")
                    print("Failed to get foreign posts")
        else:
            # foreign user
            # grab request user information from request header
            try:
                foreign_user_url = request.META["HTTP_X_REQUEST_USER_ID"]
                # foreign user in our db, get all public posts and posts that
                # are visible to or such posts' firends to this foreign user profile
                foreign_user_profile = UserProfile.objects.get(url=foreign_user_url)
                result = list(
                    self.queryset.filter(visibility="PUBLIC")
                ) + Post.not_own_posts_visible_to_me(foreign_user_profile)
                result = result + get_request_user_foaf_post(foreign_user_url)
            except UserProfile.DoesNotExist:
                # foreign user is not in our db
                # directly return public
                result = list(self.queryset.filter(visibility="PUBLIC"))
                result = result + get_request_user_foaf_post(foreign_user_url)
            except KeyError:
                return Response(
                    {"query": "posts", "success": False, "message": "No X-Request-User-ID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        result = list(set(result))  # remove duplication
        serializer = PostSerializer(result, many=True)
        data = serializer.data + foreign_posts
        return Response({"query": "posts", "count": len(data), "posts": data})

    # pylint: disable=too-many-locals
    # pylint: disable=invalid-name
    @action(detail=True, methods=["GET"], name="get_author_id_posts")
    def get_author_id_posts(self, request, pk):
        """
        GET /author/{author_id}/posts
        """
        # target_posts are posts created by author with id = pk
        target_posts = None

        # check if local user
        is_local = False
        try:
            request.user.server
        except User.server.RelatedObjectDoesNotExist:  # pylint: disable=no-member
            is_local = True

        result = []
        if is_local:
            if pk.isdigit():
                # local user
                # find all PUBLIC and SERVERONLY post create by this author with id=pk
                # add not_own_posts_visible_to_me posts
                pk = User.objects.get(pk=pk).profile.id
                if int(request.user.profile.id) == int(pk):
                    # add unlisted posts
                    result = Post.objects.filter(author=pk)
                else:
                    target_posts = self.queryset.filter(author=pk)
                    result = list(
                        target_posts.filter(Q(visibility="PUBLIC") | Q(visibility="SERVERONLY"))
                    ) + Post.not_own_posts_visible_to_me(
                        request.user.profile, queryset=target_posts
                    )
            else:
                # foreign user
                try:
                    parsed_url = urlparse(pk)
                    foreign_server = Server.objects.get(
                        url="{}://{}".format(parsed_url.scheme, parsed_url.netloc)
                    )
                    foreign_post_id = parsed_url.path.split("/")[-1]
                    response = ForeignServerHttpUtils.get(
                        foreign_server,
                        "/author/{}/posts".format(foreign_post_id),
                        headers={"X-Request-User-ID": request.user.profile.get_url()},
                    )
                    if response.status_code == 200:
                        return Response(response.json())
                    else:
                        return Response(
                            {
                                "query": "getAuthorPost",
                                "success": False,
                                "message": "Foreign server error",
                                "error": json.dumps(response.json()),
                            },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )
                except Server.DoesNotExist:
                    return Response(
                        {"succcess": False, "message": "Foreign server does not exist."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        else:
            # foreign user
            # grab request user information from request header
            # print(request.META)
            pk = User.objects.get(pk=pk).profile.id
            target_posts = self.queryset.filter(author=pk)
            try:
                foreign_user_url = request.META["HTTP_X_REQUEST_USER_ID"]
                # foreign user in our db, get all public posts created by author with id=pk
                foreign_user_profile = UserProfile.objects.get(url=foreign_user_url)
                result = list(
                    target_posts.filter(Q(visibility="PUBLIC"))
                ) + Post.not_own_posts_visible_to_me(foreign_user_profile, queryset=target_posts)
                # plus remote foaf
                result = result + get_request_user_foaf_post_belong_local_author(
                    foreign_user_url, pk
                )
            except UserProfile.DoesNotExist:
                # foreign user is not in our db
                # directly return public
                result = list(target_posts.filter(visibility="PUBLIC"))
                result = result + get_request_user_foaf_post_belong_local_author(
                    foreign_user_url, pk
                )
            except KeyError:
                return Response(
                    {"query": "posts", "success": False, "message": "No X-Request-User-ID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        result = list(set(result))  # remove duplication
        serializer = PostSerializer(result, many=True)
        data = serializer.data
        return Response({"query": "posts", "count": len(data), "posts": data})

    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    def retrieve(self, request, post_id):
        """
        GET /posts/{post_id}
        """
        # check if local user

        is_local = False
        try:
            request.user.server
        except User.server.RelatedObjectDoesNotExist:  # pylint: disable=no-member
            is_local = True
        if is_local:
            if post_id.isdigit():
                # check if acessible
                post_obj = get_object_or_404(Post, pk=post_id)
                if post_obj.is_accessible(post_obj, request.user.profile):
                    serializer = PostSerializer(post_obj)
                    return Response({"query": "post", "count": 1, "posts": [serializer.data]})
                else:
                    return Response(
                        {"query": "posts", "success": False, "message": "Post not accessible"},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            else:
                try:
                    # parse foreign user id
                    parsed_url = urlparse(post_id)
                    local_url = request.user.profile.get_url()
                    headers = {"X-Request-User-ID": str(local_url)}
                    foreign_server = Server.objects.get(
                        url="{}://{}".format(parsed_url.scheme, parsed_url.netloc)
                    )
                    response = requests.get(
                        "{}{}".format(foreign_server.endpoint, parsed_url.path),
                        auth=(
                            foreign_server.foreign_db_username,
                            foreign_server.foreign_db_password,
                        ),
                        headers=headers,
                    )
                    if response.status_code != 200:
                        logger.error(response.content)
                        return Response(
                            {"query": "getPost", "success": False, "error": response.content},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )
                    return Response(response.json())
                    # foreignsever does not exist
                except Server.DoesNotExist:
                    return Response(
                        {"succcess": False, "message": "Foreign server does not exist."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except requests.exceptions.RequestException:
                    return Response(
                        {
                            "succcess": False,
                            "message": "Failed to retrieve foreign server profile.",
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
        else:
            # foreign user
            post_obj = get_object_or_404(Post, pk=post_id)
            try:
                # grab request user information from request header
                foreign_user_url = request.META["HTTP_X_REQUEST_USER_ID"]

                # check if it is remote relationsip
                is_foaf = post_obj.author.check_remote_foaf_relationship(foreign_user_url)

                # foreign user in our db
                foreign_user_profile = UserProfile.objects.get(url=foreign_user_url)
                if post_obj.is_accessible(post_obj, foreign_user_profile) or is_foaf:
                    serializer = PostSerializer(post_obj)
                    return Response({"query": "post", "count": 1, "posts": [serializer.data]})
                else:
                    return Response(
                        {"query": "posts", "success": False, "message": "Post not accessible"},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            # foreign user is not in our db
            except UserProfile.DoesNotExist:
                if post_obj.visibility == "PUBLIC" or is_foaf:
                    serializer = PostSerializer(post_obj)
                    return Response({"query": "post", "post": serializer.data})
                else:
                    return Response(
                        {"query": "posts", "success": False, "message": "Post not accessible"},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            except KeyError:
                return Response(
                    {"query": "posts", "success": False, "message": "No X-Request-User-ID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    @action(detail=True, methods=["PUT"], name="partial_update")
    def partial_update(self, request, post_id):
        """
        PUT /posts/:id
        """
        # request.data = request.data.copy()
        body = request.data
        query = body.get("query", None)
        post_data = body.get("post", {})
        if query != "updatePost":
            return Response(data={"success": False, "msg": "Unknown query"}, status=400)
        post = get_object_or_404(Post, pk=post_id)
        if request.user.profile.id != post.author.id:
            return Response(
                data={"success": False, "msg": "current user is not able to update this post"},
                status=405,
            )
        if post_id.isdigit():
            # override partial_update
            serializer = PostSerializer(
                instance=post, data=post_data, partial=True, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response({"query": "updatePost", "count": 1, "posts": serializer.data})
            else:
                return Response(data={"success": False, "msg": serializer.errors}, status=400)
        else:
            return Response(
                data={"success": False, "msg": "Method is not allowed for foreign posts"},
                status=405,
            )

    def destroy(self, request, post_id, *args, **kwargs):
        if post_id.isdigit():
            pk = int(post_id)
            post = get_object_or_404(Post, pk=pk)
            if post.author.id == request.user.profile.id:
                self.perform_destroy(post)
                return Response(status=204)
            else:
                return Response(data={"success": False, "msg": "Forbidden access"}, status=403)
        else:
            return Response(
                data={"success": False, "msg": "Method is not allowed for foreign posts"},
                status=405,
            )


def get_request_user_foaf_post(request_user_full_id):
    result = []
    try:
        # in this case request_user_id should be foreign user id
        request_user_host_name = "{uri.scheme}://{uri.netloc}".format(
            uri=urlparse(request_user_full_id)
        )
        foreign_server = Server.objects.get(url=request_user_host_name)
        request_user_id = request_user_full_id.split("/author/")[-1]
        # print(request_user_id, "request_user_id")

        # fetch friendlist
        resp = ForeignServerHttpUtils.get(foreign_server, "/author/" + request_user_id + "/friends")
        if resp.status_code != 200:
            raise Exception("failed getting the friend_list")
        request_user_friend_list = resp.json()["authors"]
        # request_user_friend_list = [friend["id"] for friend in resp.json()["authors"]]
        # print(request_user_friend_list)

        local_users = UserProfile.objects.filter(host=None)
        # print(local_users)
        for local_user in local_users:
            local_author_friend_list = list(local_user.get_friends().values_list("url", flat=True))
            intersection_friends = list(
                set(request_user_friend_list) & set(local_author_friend_list)
            )
            if len(intersection_friends) > 0:
                result.extend(
                    list(Post.objects.filter(author=local_user, unlisted=False, visibility="FOAF"))
                )
        # print(result)
        return result
    except Exception as some_error:
        print(some_error, "foaf1 error")
        return result


def get_request_user_foaf_post_belong_local_author(request_user_full_id, local_author_profile_id):
    # in this case request_user_id should be foreign user id
    try:
        # find the server first
        request_user_host_name = "{uri.scheme}://{uri.netloc}".format(
            uri=urlparse(request_user_full_id)
        )
        foreign_server = Server.objects.get(url=request_user_host_name)
        request_user_id = request_user_full_id.split("/author/")[-1]
        # print(request_user_id, "request_user_id")

        # fetch friendlist
        resp = ForeignServerHttpUtils.get(foreign_server, "/author/" + request_user_id + "/friends")
        if resp.status_code != 200:
            raise Exception("failed getting the friend_list")
        request_user_friend_list = resp.json()["authors"]
        # request_user_friend_list = [friend["id"] for friend in resp.json()["authors"]]
        # print(request_user_friend_list)

        local_author_friend_list = list(
            UserProfile.objects.get(id=local_author_profile_id)
            .get_friends()
            .values_list("url", flat=True)
        )
        # print(local_author_friend_list)

        intersection_friends = list(set(request_user_friend_list) & set(local_author_friend_list))
        # print(intersection_friends)

        if len(intersection_friends) > 0:  # is friend of friend
            result = list(
                Post.objects.filter(
                    author_id=local_author_profile_id, unlisted=False, visibility="FOAF"
                )
            )
        else:  # is not friend of friend
            result = []

        # print(result)
        return result

    except Exception as some_error:
        print(some_error, "foaf2 error")
        return []
