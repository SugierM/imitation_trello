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


permission_classes = [IsAuthenticated, IsRoleAuthorized]


# -------------------------------------------------------------- BOARDS ------------------------------------------------------------------------------------------------
class BoardCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardCreateSerialzier


class BoardView(generics.RetrieveUpdateAPIView):
    serializer_class = BoardSerializer
    permission_classes = permission_classes
    lookup_field = "pk"
    queryset = Board.objects.all()


class BoardDestroyView(generics.DestroyAPIView):
    serializer_class = BoardSerializer
    permission_classes = permission_classes
    queryset = Board.objects.all()


class BoardListView(generics.ListAPIView):
    serializer_class = BoardsListSerializer
    permission_classes = permission_classes
    
    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(memberships__user=user)

    
# -------------------------------------------------------------- ELEMENTS -----------------------------------------------------------------------------------------------
class ElementCreateView(generics.CreateAPIView):
    serializer_class = ElementCreateSerializer
    permission_classes = permission_classes
    queryset = Element.objects.all()

class ElementView(generics.RetrieveUpdateAPIView): 
    serializer_class = ElementSerializer
    permission_classes = permission_classes
    lookup_field = "pk"
    queryset = Element.objects.all()


class ElementDestroyView(generics.DestroyAPIView):
    serializer_class = ElementSerializer
    permission_classes = permission_classes
    queryset = Element.objects.all()


class ElementListView(generics.ListAPIView):
    serializer_class = ElementSerializer
    permission_classes = permission_classes

    def get_queryset(self):
        board_id = self.kwargs.get("board")
        return Element.objects.filter(board__id=board_id)


# ---------------------------------------------------------------- TASK -------------------------------------------------------------------------------------------------

class TaskView(generics.RetrieveUpdateAPIView): 
    serializer_class = TaskSerializer
    permission_classes = permission_classes
    lookup_field = "pk"
    queryset = Task.objects.all()


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = permission_classes
    
    def get_queryset(self):
        element_id = self.kwargs.get("element")
        return Task.objects.filter(element__id=element_id)


class TaskCreateView(generics.CreateAPIView):
    permission_classes = permission_classes
    serializer_class = TaskCreateSerializer
    queryset = Task.objects.all()


class TaskDestroyView(generics.DestroyAPIView):
    permission_classes = permission_classes
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


# --------------------------------------------------------------- SUBTASK -----------------------------------------------------------------------------------------------


# ------------------------------------------------------------- ATTACHMENT ----------------------------------------------------------------------------------------------


# -------------------------------------------------------------- COMMENTS -----------------------------------------------------------------------------------------------# 
