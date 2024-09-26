from django.http import JsonResponse
import json
from rest_framework import status, generics
from Users.serializers import UserProfileSerializer
from Users.models import User

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    # def perform_create(self, serializer):
    #     pass


class UserView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        first_name = self.kwargs.get("first_name")
        return User.objects.filter(first_name=first_name)
    

# AFTER LOGGING IN

# class UserUpdateView(generics.UpdateAPIView):
#     queryset = User.objects.all()
