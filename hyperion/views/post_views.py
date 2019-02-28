
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

    @action(detail=True, methods=['POST'], name='post_auth_posts')
    def post_auth_posts(self, request):
        '''
        response: {'status': 'success', 'post': data}
        '''
        if request.user.id:
            body = request.data
            post_query = body.get('query', None)
            post_data = body.get('post', None)
            if post_query == 'createPost' and post_query:
                post_data['visible_to'] = post_data.get('visible_to', [])
                serializer = PostSerializer(data=post_data)
                return Response(post_data)
                if serializer.is_valid():
                    return Response(
                        {'status': 'success',
                         'post': serializer.data
                         })
                else:
                    return Response(
                        {'status': 'failed',
                         'errors': serializer.errors
                         })

        return Response({'status': '401'})

    @action(detail=True, methods=['GET'], name='get_auth_posts')
    def get_auth_posts(self, request):
        '''
        response: {'status': 'success', 'posts': data}
        '''
        if request.user.id:
            serializer = PostSerializer(
                self.queryset.filter(author=request.user.profile),
                many=True
            )
            return Response({'status': 'success', 'posts': serializer.data})
        else:
            return Response({'status': '401'})

    def list(self, request):
        '''
        response: {'status': 'success', 'posts': data}
        '''
        if request.user.id:
            response = super().list(request)
            data = response.data
            response.data = {'status': 'success', 'posts': data}
            return response
        else:
            return Response({'status': '401'})

    def retrieve(self, request, pk):
        '''
        response: {'status': 'success', 'post': data}
        '''
        if request.user.id:
            response = super().retrieve(request, pk)
            data = response.data
            response.data = {'status': 'success', 'post': data}
            return response
        else:
            return Response({'status': '401'})

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
