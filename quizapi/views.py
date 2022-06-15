import imp
from rest_framework import generics
from rest_framework.permissions import AllowAny
from users.models import CustomUser
from .serializers import UserSerializer

class UserCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)