from django.http import JsonResponse
import json
from rest_framework import status, generics
from rest_framework.views import APIView
from Users.serializers import *
from Users.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .permissions import IsOwnProfile
from django.shortcuts import get_object_or_404


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    # def perform_create(self, serializer):
    #     pass


class UserSearchNameView(generics.ListAPIView):
    serializer_class = UserLookupSerializer
    
    def get_queryset(self):
        first_name = self.kwargs.get("first_name")
        return User.objects.filter(first_name=first_name) # Does not make sense to look up something based only on name
    

class UserProfile(APIView):
    permission_classes = [IsAuthenticated, IsOwnProfile]
    serializer_class = UserProfileSerializer

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    

class UserLookupView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        else:
            return Response({"invalid": "Invalid data"}, status=404)
             
class OtherUserPorfile(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OtherUserProfileSerializer
    queryset = User.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user1"] = self.request.user
        return context


# AFTER LOGGING IN

# class UserUpdateView(generics.UpdateAPIView):
#     queryset = User.objects.all()
