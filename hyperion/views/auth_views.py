from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed

from hyperion.serializers import UserSerializer
from hyperion.authentication import HyperionBasicAuthentication


class AuthView(APIView):
    authentication_classes = (HyperionBasicAuthentication,)
    permission_classes = (IsAuthenticated, AllowAny)

    def get(self, request):
        user = UserSerializer(request.user, context={'request': request})
        content = {'msg': 'success', 'user': user.data}
        return Response(content)

    def post(self, request):
        user = UserSerializer(request.user, context={'request': request})
        content = {'msg': 'success', 'user': user.data}
        return Response(content)
