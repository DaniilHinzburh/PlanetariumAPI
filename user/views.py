from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserViewSet(generics.CreateAPIView):
    serializer_class = UserSerializer
