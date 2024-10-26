from django.http import JsonResponse
import json
from rest_framework import status, generics
from rest_framework.views import APIView
from Users.serializers import UserProfileSerializer, UserRegisterSerializer, UserLookupSerializer
from Users.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .permissions import IsOwnProfile

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    # def perform_create(self, serializer):
    #     pass


class UserSearchNameView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        first_name = self.kwargs.get("first_name")
        return User.objects.filter(first_name=first_name)
    
class UserLoggedInView(APIView):
    """
    Test view
    """
    # permission_classes = [IsAuthenticated]
    # serializer_class = UserSerializer
    # queryset = User.objects.all()

    # def get(self, request):
    #     user = request.user
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)

class UserProfile(APIView):
    permission_classes = [IsAuthenticated, IsOwnProfile]
    serializer_class = UserProfileSerializer

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
class UserLookupView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLookupSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        else:
            return Response({"invalid": "Invalid data"}, status=404)
             

# AFTER LOGGING IN

# class UserUpdateView(generics.UpdateAPIView):
#     queryset = User.objects.all()
