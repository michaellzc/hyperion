# pylint: disable=arguments-differ
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from hyperion.authentication import HyperionBasicAuthentication
from hyperion.serializers import CommentSerializer
from hyperion.models import Comment, Post, UserProfile


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
        # get current autheticated user
        try:
            body = request.data
            comment_query = body.get("query", None)
            comment_data = body.get("comment", None)
            comment_data["post"] = pk
            server = request.user.server
        except User.server.RelatedObjectDoesNotExist:  # pylint: disable=no-member
            # local host
            author_profile = request.user.profile
            comment_data["author"] = str(request.user.profile.id)
        except Exception as other_errs:  # pylint: disable=broad-except
            return Response(
                {"query": comment_query, "success": False, "message": str(other_errs)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            # foreign server
            try:
                author_profile = UserProfile.objects.get(url=comment_data["author"]["id"])
            except UserProfile.DoesNotExist:
                # foreign user is not in our db
                try:
                    author_profile = UserProfile.objects.create(
                        display_name=comment_data["author"]["display_name"],
                        host=server,
                        url=comment_data["author"]["id"],
                    )
                except Exception as some_error:  # pylint: disable=broad-except
                    raise Exception("create author profile failed, reason: " + str(some_error))
            comment_data["author"] = str(author_profile.id)

        post_data = get_object_or_404(Post, pk=pk)
        accessible = post_data.is_accessible(post_data, author_profile)
        if comment_query == "addComment" and comment_data and accessible:
            serializer = CommentSerializer(data=comment_data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"query": "addComment", "success": True, "message": "Comment Created"}
                )
            else:
                return Response(
                    {"query": "addComment", "success": False, "message": serializer.errors},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        elif comment_query == "addComment" and comment_data and not accessible:
            return Response(
                {"query": "addComment", "success": False, "message": "Post not accessible"},
                status=status.HTTP_403_FORBIDDEN,
            )
        else:
            return Response(
                {"query": comment_query, "success": False, "message": "bad request"},
                status=status.HTTP_400_BAD_REQUEST,)