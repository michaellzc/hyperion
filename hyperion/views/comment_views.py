# pylint: disable=arguments-differ,too-many-locals,too-many-return-statements
from urllib.parse import urlparse
from requests.exceptions import RequestException

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status

from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from hyperion.authentication import HyperionBasicAuthentication
from hyperion.serializers import CommentSerializer
from hyperion.models import Comment, Post, UserProfile, Server
from hyperion.utils import ForeignServerHttpUtils


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (HyperionBasicAuthentication,)
    permission_classes = (IsAuthenticated, AllowAny)

    @action(detail=True, methods=["POST"], name="new_comment")
    def new_comment(self, request, pk=None):  # pylint: disable=invalid-name
        """
        POST /posts/{post_id}/comments
        """
        is_local = False

        try:
            # check if authenticated user is a server or local user
            request.user.server
        except User.server.RelatedObjectDoesNotExist:  # pylint: disable=no-member
            # local user shoud not have an one-to-one relationship with Server
            is_local = True

        body = request.data
        comment_data = body.get("comment", None)
        author = comment_data.get("author", None)
        author_id = author.get("id", None)
        post_id = body.get("post", None)
        post_url = urlparse(post_id)
        author_profile = None

        if is_local:
            # handle local author request
            post_url_host = "{}://{}".format(post_url.scheme, post_url.netloc)
            if post_url_host == settings.HYPERION_HOSTNAME:
                # comment on local post
                post_pk = post_url.path.split("/")[-1]
                comment_data["post"] = post_pk
                author_profile = request.user.profile
                comment_data["author"] = str(author_profile.id)
            else:
                # comment on foreign post
                try:
                    foreign_server = Server.objects.get(url=post_url_host)
                    post_pk = post_url.path.split("/")[-1]
                    resp = ForeignServerHttpUtils.post(
                        foreign_server, "/posts/{}/comments".format(post_pk), json=body
                    )
                    if resp.status_code != 200:
                        print(resp.content)
                        print(resp.json())
                        return Response(
                            {"query": "addComment", "success": False, "message": resp.content},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )
                    return Response(
                        {"query": "addComment", "success": True, "message": "Comment Created"}
                    )
                except RequestException as exception:
                    return Response(
                        {
                            "query": "addComment",
                            "success": False,
                            "message": "Not my fault.",
                            "error": exception,
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                except Server.DoesNotExist:
                    return Response(
                        {
                            "query": "addComment",
                            "success": False,
                            "message": "Target foreign server is not support",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        else:
            # handle foreign server request
            server = request.user.server
            author_profile, _ = UserProfile.objects.filter(Q(url=author_id)).get_or_create(
                url=author_id, display_name=author.get("display_name", None), host=server
            )
            post_pk = post_url.path.split("/")[-1]
            comment_data["post"] = post_pk
            comment_data["author"] = str(author_profile.id)

        post_data = get_object_or_404(Post, pk=post_pk)
        accessible = post_data.is_accessible(post_data, author_profile)

        # validate query name
        if body.get("query", None) != "addComment":
            return Response(
                {"query": "addComment", "success": False, "message": "Bad Request"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        # validate accessibility
        if not accessible:
            return Response(
                {"query": "addComment", "success": False, "message": "Forbidden access"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CommentSerializer(data=comment_data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                {"query": "addComment", "success": False, "message": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        return Response({"query": "addComment", "success": True, "message": "Comment Created"})
