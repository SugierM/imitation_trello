
from django.http import JsonResponse
import json
from rest_framework import status, generics
from Users.serializers import UserProfileSerializer


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
