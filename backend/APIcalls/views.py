from django.shortcuts import render
from django.http import JsonResponse
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status, generics
from Users.serializers import UserProfileSerializer, UserProfileViewSerializer
from Users.models import User

class UserCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileViewSerializer
    lookup_field = 'first_name'



def test(request, *args, **kwargs):

    body = request.body
    data = {}
    try:
        data = json.loads(body)
    except: 
        pass
    data['headers'] = dict(request.headers)
    data['params'] = request.GET
    return JsonResponse(data)
