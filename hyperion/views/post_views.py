# pylint: disable=arguments-differ
import requests
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets

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
                response = requests.get(foreign_url, headers=headers)
                if response.status_code == 200:
                    body = response.json()
                    print(body,'response.body htz')
                    posts = body.get("posts", [])
                    foreign_posts += posts
                else:
                    return Response(
                        {"query": "posts", "success": False, "message": response.content})
        else:
            # foreign user
            # grab request user information from request header
            try:
                foreign_user_url = request.META["HTTP_X_REQUEST_USER_ID"]
                # foreign user in our db, get all public posts and posts that
                # are visible to or such posts' firends to this foreign user profile
                foreign_user_profile = UserProfile.objects.get(url=foreign_user_url)
                result = list(self.queryset.filter(
                    visibility="PUBLIC"
                )) + Post.not_own_posts_visible_to_me(foreign_user_profile)
            except UserProfile.DoesNotExist:
                # foreign user is not in our db
                # directly return public
                result = self.queryset.filter(visibility="PUBLIC")
            except KeyError:
                return Response(
                    {"query": "posts", "success": False, "message": 'No X-Request-User-ID'})

        result = list(set(result))  # remove duplication
        serializer = PostSerializer(result, many=True)
        data = serializer.data + foreign_posts
        return Response({"query": "posts", "count": len(data), "posts": data})

    def list(self, request):
        """
        GET /posts
        """
        response = super().list(request)
        data = response.data
        response.data = {"query": "posts", "count": len(data), "posts": data}
        return response

    def retrieve(self, request, pk):
        """
        GET posts/{id}/
        """
        post_obj = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post_obj)
        return Response({"query": "post", "post": serializer.data})

    def destroy(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if post.author.id == request.user.profile.id:
            self.perform_destroy(post)
            return Response(status=204)
        else:
            return Response(data={"success": False, "msg": "Forbidden access"}, status=403)
