from django.shortcuts import render, redirect
from .models import Board, BoardMembership, Task, Element
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import BoardSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsRoleAuthorized
from django.contrib import messages
from .serializers import *


class PermissionDefaultMixin():
    permission_classes = [IsAuthenticated, IsRoleAuthorized]


# -------------------------------------------------------------- BOARDS ------------------------------------------------------------------------------------------------
class BoardCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardCreateSerialzier

class BoardView(generics.RetrieveUpdateAPIView, PermissionDefaultMixin):
    serializer_class = BoardSerializer
    lookup_field = "pk"
    queryset = Board.objects.all()


class BoardDestroyView(generics.DestroyAPIView, PermissionDefaultMixin):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()


class BoardListView(generics.ListAPIView, PermissionDefaultMixin):
    serializer_class = BoardsListSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(memberships__user=user)

    
# -------------------------------------------------------------- ELEMENTS -----------------------------------------------------------------------------------------------
class ElementCreateView(generics.CreateAPIView, PermissionDefaultMixin):
    serializer_class = ElementCreateSerializer
    queryset = Element.objects.all()

class ElementView(generics.RetrieveUpdateAPIView, PermissionDefaultMixin): 
    serializer_class = ElementSerializer
    lookup_field = "pk"
    queryset = Element.objects.all()


class ElementDestroyView(generics.DestroyAPIView, PermissionDefaultMixin):
    serializer_class = ElementSerializer
    queryset = Element.objects.all()


class ElementListView(generics.ListAPIView, PermissionDefaultMixin):
    serializer_class = ElementSerializer

    def get_queryset(self):
        board_id = self.kwargs.get("board")
        return Element.objects.filter(board__id=board_id)


    
# class BoardView(generics.ListAPIView):
#     serializer_class = BoardSerializer
#     queryset = Board.objects.all()
    

# class BoardViewSet(ModelViewSet, PermissionDefaultMixin):
#     serializer_class = BoardSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return Board.objects.filter(memberships__user=user)

# class TaskViewSet(ModelViewSet, PermissionDefaultMixin):
#     serializer_class = TaskSerializer

#     def get_queryset(self):
#         return Task.objects.filter(element__board__memberships__user=self.request.user)
    
#     def create(self, request, *args, **kwargs):
#         element_id = request.data.get('element')
#         try:
#             element = Element.objects.get(id=element_id)
#         except Element.DoesNotExist:
#             return Response({"detail": "Element not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         board = element.board
        
#         if not BoardMembership.objects.filter(user=request.user, board=board, role__in=["ADMIN", "EDITOR"]).exists():
#             return Response({"detail": "You don't have permissions for that"}, status=status.HTTP_403_FORBIDDEN)
        
        
#         response = super().create(request, *args, **kwargs)

#         if response.status_code == status.HTTP_201_CREATED:
#             return redirect('task-list') # CHANGE IT IN THE FUTURE (it's to avoid multiple 'creates' during testing)

#         return response