# pylint: disable=arguments-differ

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from hyperion.authentication import HyperionBasicAuthentication
from hyperion.serializers import CommentSerializer, UserProfileSerializer
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
    def new_comment(self, request, pk=None): # pylint: disable=invalid-name
        """
        POST /posts/{post_id}/comments
        """
        body = request.data
        comment_query = body.get("query", None)
        comment_data = body.get("comment", None)
        comment_data['post'] = str(pk)
        post_data = Post.objects.get(pk=pk)
        accessible = post_data.is_accessible(post_data, request.user.profile)

        if comment_query == "addComment" and comment_data and accessible:
            serializer = CommentSerializer(data=comment_data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "query": "addComment",
                        "success": True,
                        "message": "Comment Created",
                    }
                )
            else:
                return Response(
                    {
                        "query": "addComment",
                        "success": False,
                        "message": serializer.errors,
                    }, status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        elif comment_query == "addComment" and comment_data and not accessible:
            return Response(
                {
                    "query": "addComment",
                    "success": False,
                    "message": "Post not accessible",
                }, status=status.HTTP_403_FORBIDDEN
            )
