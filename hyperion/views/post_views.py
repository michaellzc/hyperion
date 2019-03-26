# pylint: disable=arguments-differ
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
        response = super().list(request)
        data = response.data
        response.data = {"query": "posts", "count": len(data), "posts": data}
        return response

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
                foreign_url = server.author.profile.url + "/api/author/posts"
                local_url = request.user.profile.get_url()
                headers = {"X-Request-User-ID": str(local_url)}
                response = requests.get(
                    foreign_url,
                    headers=headers,
                    auth=(server.foreign_db_username, server.foreign_db_password),
                )
                if response.status_code == 200:
                    body = response.json()
                    posts = body.get("posts", [])
                    foreign_posts += posts
                else:
                    return Response(
                        {"query": "posts", "success": False, "message": response.content},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
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
            except UserProfile.DoesNotExist:
                # foreign user is not in our db
                # directly return public
                result = list(self.queryset.filter(visibility="PUBLIC"))
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
        try:
            pk = User.objects.get(pk=pk).profile.id
        except User.DoesNotExist:
            return Response(
                {
                    "query": "posts",
                    "success": False,
                    "message": "Only can get the posts from our user (id exists)",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # target_posts are posts created by author with id = pk
        target_posts = None

        # check if local user
        result = []
        try:
            request.user.server
        except User.server.RelatedObjectDoesNotExist:  # pylint: disable=no-member
            # local user
            # find all PUBLIC and SERVERONLY post create by this author with id=pk
            # add not_own_posts_visible_to_me posts
            if int(request.user.profile.id) == int(pk):
                # add unlisted posts
                target_posts = Post.objects.filter(author=pk)
            else:
                target_posts = self.queryset.filter(author=pk)
            result = list(
                target_posts.filter(Q(visibility="PUBLIC") | Q(visibility="SERVERONLY"))
            ) + Post.not_own_posts_visible_to_me(request.user.profile, queryset=target_posts)
        else:
            # foreign user
            # grab request user information from request header
            target_posts = self.queryset.filter(author=pk)
            try:
                foreign_user_url = request.META["HTTP_X_REQUEST_USER_ID"]
                # foreign user in our db, get all public posts created by author with id=pk
                foreign_user_profile = UserProfile.objects.get(url=foreign_user_url)
                result = list(
                    target_posts.filter(Q(visibility="PUBLIC"))
                ) + Post.not_own_posts_visible_to_me(foreign_user_profile, queryset=target_posts)
            except UserProfile.DoesNotExist:
                # foreign user is not in our db
                # directly return public
                result = list(target_posts.filter(visibility="PUBLIC"))
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
    def retrieve(self, request, pk):
        """
        GET /posts/{post_id}
        """
         # check if local user
        try:
            request.user.server
        except User.server.RelatedObjectDoesNotExist:  # pylint: disable=no-member
            post_obj = get_object_or_404(Post, pk=pk)
            if post_obj.is_accessible(post_obj, request.user.profile):
                serializer = PostSerializer(post_obj)
                return Response(
                    {"query": "post","post": serializer.data})
            else:
                return Response(
                    {"query": "posts", "success": False, "message": "Post not accessible"},
                    status=status.HTTP_403_FORBIDDEN)
        else:
            # foreign user
            post_obj = get_object_or_404(Post, pk=pk)
            try:
                # grab request user information from request header
                foreign_user_url = request.META["HTTP_X_REQUEST_USER_ID"]
                # foreign user in our db
                foreign_user_profile = UserProfile.objects.get(url=foreign_user_url)
                if post_obj.is_accessible(post_obj, foreign_user_profile):
                    serializer = PostSerializer(post_obj)
                    return Response(
                        {"query": "post", "post": serializer.data})
                else:
                    return Response(
                        {"query": "posts", "success": False, "message": "Post not accessible"},
                        status=status.HTTP_403_FORBIDDEN)

            # foreign user is not in our db
            except UserProfile.DoesNotExist:
                if post_obj.visibility == "PUBLIC":
                    serializer = PostSerializer(post_obj)
                    return Response(
                        {"query": "post", "post": serializer.data})
                else:
                    return Response(
                        {"query": "posts", "success": False, "message": "Post not accessible"},
                        status=status.HTTP_403_FORBIDDEN)
            except KeyError:
                return Response(
                    {"query": "posts", "success": False, "message": 'No X-Request-User-ID'},
                    status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if post.author.id == request.user.profile.id:
            self.perform_destroy(post)
            return Response(status=204)
        else:
            return Response(data={"success": False, "msg": "Forbidden access"}, status=403)
