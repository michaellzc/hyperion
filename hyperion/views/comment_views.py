# pylint: disable=arguments-differ

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User

from hyperion.authentication import HyperionBasicAuthentication
from hyperion.serializers import CommentSerializer
from hyperion.models import Comment, Post, Server, UserProfile


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
        try:
            # get request info
            body = request.data
            comment_query = body.get("query", None)
            comment_data = body.get("comment", None)
            comment_data['post'] = str(pk)
            # commenter is in our local host
            if comment_data["author"]["host"] == settings.HYPERION_HOSTNAME:
                author_profile = request.user.profile
            # commenter is in remote host
            else:
            # check if the author's host is trusted by us
                try:
                    server = Server.objects.get(name=comment_data["author"]["host"])
                except Server.DoesNotExist:
                    raise Exception("the author's server is not verified by us")
            # check if we already have this remote user profile after checking server
                try:
                    author_profile = UserProfile.objects.get(url=comment_data["author"]["id"])
                    has_author_profile = True
                except UserProfile.DoesNotExist:
                    # if we doesn't have this user profile
                    # (may also check if user exist in remote server
                    has_author_profile = False
                # create copy of a remote user profile
                if not has_author_profile:
                    print("create_remote_profile")
                    try:
                        author_profile = UserProfile.objects.create(
                            display_name=comment_data["author"]["display_name"],
                            host=server,
                            url=comment_data["author"]["id"],
                        )
                    except Exception as some_error:
                        raise Exception(
                            "create author profile failed, reason: " + str(some_error)
                        )
        except User.DoesNotExist:
            return Response(
                    {
                        "query": "addComment",
                        "success": False,
                        "message": "User does not exist",
                    }, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except Exception as some_error:
            return Response(
                    {
                        "query": "addComment",
                        "success": False,
                        "message": str(some_error),
                    }, status=status.HTTP_400_BAD_REQUEST
            )
        
        '''
        End of handle author_profile
        Starting handle 
        Post_data is always on our host.author_profile may not.
        '''
        post_data = Post.objects.get(pk=pk)
        accessible = post_data.is_accessible(post_data, author_profile)
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
