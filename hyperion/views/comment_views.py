# pylint: disable=arguments-differ

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets

from hyperion.authentication import HyperionBasicAuthentication
from hyperion.serializers import PostSerializer
from hyperion.models import Comment

from urllib.parse import urlparse

class CommentViewSet(viewsets.ModelViewSet):
     """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (HyperionBasicAuthentication,)
    permission_classes = (IsAuthenticated, AllowAny)

    @action(detail=True, methods=["POST"], name="new_comment")
    def new_comment(self, request):
        body = request.data
        comment_query = body.get("query", None)
        comment_data = body.get("comment", None)
        author = comment_data.get("author")

        post_url = body.get("post", None)
        post_id = urlparse(post_url).path.split("/")[-1]
        post_data = Post.Objects.get(pk=post_id)
        accessible = post_data.post_accessible(post_data,author)

        if comment_query == "createComment" and comment_data and accessible:
            serializer = CommentSerializer(data=comment_data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "query": "createComment",
                        "success": True,
                        "message": "Comment Created",
                    }
                )
            else:
                return Response(
                    {
                        "query": "createComment",
                        "success": False,
                        "message": serializer.errors,
                    }
                )
        elif comment_query == "createComment" and comment_data and not accessible:
            return Response(
                    {
                        "query": "createComment",
                        "success": False,
                        "message": "Post not accessible",
                    }
                )