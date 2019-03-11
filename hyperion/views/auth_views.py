from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User

from hyperion.serializers import UserSerializer, UserSignUpSerializer
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


class CreateUserView(CreateAPIView):

    model = User
    permission_classes = [AllowAny]
    serializer_class = UserSignUpSerializer

    @staticmethod
    # https://stackoverflow.com/questions/31433989/return-copy-of-dictionary-excluding-specified-keys
    # author: mu
    def without_keys(source_dict, keys):
        return {x: source_dict[x] for x in source_dict if x not in keys}

    # https://stackoverflow.com/questions/47975001/django-rest-framework-custom-return-response
    # author: Ykh
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            CreateUserView.without_keys(serializer.data, ["password"]),
            status=status.HTTP_201_CREATED,
            headers=headers)
