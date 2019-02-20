from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed

from hyperion.serializers import UserSerializer


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
