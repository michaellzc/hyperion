from django.contrib.auth.models import User, Group
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import viewsets, decorators, authentication, views

from .serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class AuthView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, AllowAny)

    # https://stackoverflow.com/questions/18262643/adding-custom-response-headers-to-apiexception
    # https://stackoverflow.com/questions/86105/how-can-i-suppress-the-browsers-authentication-dialog
    def handle_exception(self, exc):
        if isinstance(exc, AuthenticationFailed):
            self.headers['WWW-Authenticate'] = ""
            return Response({'detail': exc.detail},
                            status=exc.status_code, exception=True)
        else:
            super(AuthView, self).handle_exception(exc)

    def get(self, request):
        user = UserSerializer(request.user, context={'request': request})
        content = {'msg': 'success', 'user': user.data}
        return Response(content)

    def post(self, request):
        user = UserSerializer(request.user, context={'request': request})
        content = {'msg': 'success', 'user': user.data}
        return Response(content)
