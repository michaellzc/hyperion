
from rest_framework import viewsets
from hyperion.serializers import PostSerializer
from hyperion.models import Post
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


    @action(detail=True, methods=['GET'], name='get_auth_posts')
    def get_auth_posts(self, request):
        if request.user.id:
            serializer = PostSerializer(
                self.queryset.filter(author=request.user.profile),
                many=True
            )
            return Response(serializer.data)
        