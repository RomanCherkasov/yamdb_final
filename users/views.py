from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from users.permissions import AdminOnly
from users.serializers import RegistrationSerializer, UsersSerializer


class RegistrationsAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        if request.data.get(
                'username'
        ) and request.data.get('username') == 'me':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'username': serializer.data.get('username'),
            'email': serializer.data.get('email')}
        return Response(data, status=status.HTTP_200_OK)


class TokenSenderAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        if request.data.get(
                'username'
        ) and request.data.get('confirmation_code'):
            user = get_object_or_404(User,
                                     username=request.data.get('username'))
            confirmation_code = request.data.get('confirmation_code')
            if default_token_generator.check_token(user, confirmation_code):
                return Response({
                    'token': str(AccessToken.for_user(user))
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'confirmation_code': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (AdminOnly,)
    filter_backends = (DjangoFilterBackend,)
    fillterset_fields = ('username',)

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        username = self.kwargs.get('pk')
        user = get_object_or_404(User, username=username)
        return user

    @action(detail=False, permission_classes=(IsAuthenticated,),
            methods=['patch', 'get'])
    def me(self, request):
        if request.method == 'GET':
            user = get_object_or_404(User, username=self.request._user)
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            user = get_object_or_404(User, username=self.request._user)
            serializer = self.get_serializer(user,
                                             data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role, partial=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
