# pylint: disable=arguments-differ

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets

from hyperion.authentication import HyperionBasicAuthentication
from hyperion.serializers import PostSerializer
from hyperion.models import Post


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (HyperionBasicAuthentication,)
    permission_classes = (IsAuthenticated, AllowAny)

    @action(detail=True, methods=['POST'], name='post_auth_posts')
    def post_auth_posts(self, request):
        '''
        POST /author/posts
        '''
        body = request.data
        post_query = body.get('query', None)
        post_data = body.get('post', None)
        if post_query == 'createPost' and post_data:
            post_data['visible_to'] = post_data.get('visible_to', [])
            serializer = PostSerializer(
                data=post_data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'query': 'createPost',
                    'success': True,
                    'message': 'Author Post Created'
                })
            else:
                return Response({
                    'query': 'createPost',
                    'success': False,
                    'message': serializer.errors
                })

    @action(detail=True, methods=['GET'], name='get_auth_posts')
    def get_auth_posts(self, request):
        '''
        GET /author/posts
        '''

        # result = list of post
        # result = self.queryset.filter(author=request.user.profile) | \
        #     self.queryset.filter(visibility ='PUBLIC') | \
        #     self.queryset.filter(visibility ='FOAF',request.user.profile in visible_to_friends_of_friends()) | \
        #     self.queryset.filter(visibility ='FRIENDS',request.user.profile in visible_to_my_friends()) | \
        #     self.queryset.filter(visibility ='PRIVATE',request.user.profile in visible_to)
        result = self.queryset.filter(author=request.user.profile)\
        + Post.visible_to_private(request.user.profile) \ 
        + Post.visible_to_public(request.user.profile) \
        + Post.visible_to_friends_of_friends(request.user.profile) \
        + Post.visible_to_friends(request.user.profile)
        serializer = PostSerializer(result, many=True)
       
        return Response({
            'query': 'posts',
            'count': len(serializer.data),
            'posts': serializer.data
        })

    def list(self, request):
        '''
        GET /posts
        '''
        response = super().list(request)
        data = response.data
        response.data = {'query': 'posts', 'count': len(data), 'posts': data}
        return response

    def retrieve(self, request, pk):
        '''
        GET posts/{id}
        '''
        response = super().retrieve(request, pk)
        data = response.data
        response.data = {'query': 'post', 'post': data}
        return response
