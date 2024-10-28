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
from django.db.models import Q
from django.shortcuts import get_object_or_404


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]



class UserSearchView(generics.ListAPIView):
    serializer_class = UserLookupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        search_q: str = self.request.query_params.get('q', None)

        if search_q:
            queryset = User.objects.all()
            search_terms = search_q.split()
            query = Q()

            for term in search_terms:
                query |= Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(nickname__icontains=term) 
        
            queryset = queryset.filter(query)
        else:
            queryset = User.objects.none()
        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset() # Check
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

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
