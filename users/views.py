from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .serializers import RegisterSerializer, UserSerializer


User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        """Регистрация нового пользователя"""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Получаем токен
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Работать с пользователями могут только админы

class TokenView(APIView):
    permission_classes = [IsAdminUser]  # Получать токены могут только админы
    def get(self, request, *args, **kwargs):
        tokens = Token.objects.all()
        serialized_tokens = [{'user_id': token.user_id, 'key': token.key} for token in tokens]
        return Response(serialized_tokens, status=status.HTTP_200_OK)