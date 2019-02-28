from rest_framework.decorators import action
# from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from hyperion.serializers import PostSerializer
from hyperion.models import Post


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['POST'], name='post_auth_posts')
    def post_auth_posts(self, request):
        '''
        POST /author/posts
        '''
        body = request.data
        post_query = body.get('query', None)
        post_data = body.get('post', None)
        if post_query == 'createPost' and post_query:
            post_data['visible_to'] = post_data.get('visible_to', [])
            serializer = PostSerializer(data=post_data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {'query': 'createPost',
                     'success': True,
                     'message': 'Author Post Created'
                     })
            else:
                return Response(
                    {'query': 'createPost',
                     'success': False,
                     'message': serializer.errors
                     })

    @action(detail=True, methods=['GET'], name='get_auth_posts')
    def get_auth_posts(self, request):
        '''
        GET /author/posts
        '''
        serializer = PostSerializer(
            self.queryset.filter(author=request.user.profile),
            many=True
        )
        return Response({
            'query': 'visiblePosts',
            'count': len(serializer.data),
            'posts': serializer.data
        })

    def list(self, request):
        '''
        GET /posts
        '''
        response = super().list(request)
        data = response.data
        response.data = {
            'query': 'publicPosts',
            'count': len(data),
            'posts': data
        }
        return response

    def retrieve(self, request, pk):
        '''
        GET posts/{id}
        '''
        response = super().retrieve(request, pk)
        data = response.data
        response.data = {'query': 'post', 'post': data}
        return response

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
