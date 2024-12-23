from django.shortcuts import render, redirect
from .models import Board, BoardMembership, Task, Element
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from django.contrib import messages
from .serializers import *
from django.db.models import Count, Q, OuterRef, Subquery
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse


permission_classes = [IsAuthenticated, IsRoleAuthorized]


# -------------------------------------------------------------- BOARDS ------------------------------------------------------------------------------------------------
class BoardCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardCreateSerialzier


class BoardView(generics.RetrieveUpdateAPIView):
    queryset = Board.objects.annotate(
        total_elements=Count("elements"),
        completed_elements = Count("elements", filter=Q(elements__status=1)),
    )

    serializer_class = BoardSerializer
    permission_classes = permission_classes
    lookup_field = "pk"


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
    queryset = Element.objects.annotate(
        total_tasks = Count("tasks"),
        completed_tasks = Count("tasks", filter=Q(tasks__status=1)),
        postponed_tasks = Count("tasks", filter=Q(tasks__status=2))
    )
    serializer_class = ElementsSerializer
    permission_classes = permission_classes
    lookup_field = "pk"


class ElementDestroyView(generics.DestroyAPIView):
    serializer_class = ElementsBaseSerializer
    permission_classes = permission_classes
    queryset = Element.objects.all()


class ElementListView(generics.ListAPIView):
    serializer_class = ElementsBaseSerializer
    permission_classes = permission_classes

    def get_queryset(self):
        board_id = self.kwargs.get("board")
        user = self.request.user

        is_member = BoardMembership.objects.filter(user=user, board=board_id).exists()
        if not is_member:
            raise PermissionDenied("You don't have permissions to see this.")
        return Element.objects.filter(board__id=board_id)


# ---------------------------------------------------------------- TASK -------------------------------------------------------------------------------------------------

class TaskView(generics.RetrieveUpdateAPIView): 
    serializer_class = TaskBaseSerializer
    permission_classes = [IsAuthenticated, TaskAssignedOrRoleAuthorized]
    lookup_field = "pk"
    queryset = Task.objects.all()


class TaskListView(generics.ListAPIView):
    serializer_class = TaskBaseSerializer
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
    serializer_class = TaskBaseSerializer
    queryset = Task.objects.all()


# --------------------------------------------------------------- SUBTASK -----------------------------------------------------------------------------------------------


# ------------------------------------------------------------- ATTACHMENT ----------------------------------------------------------------------------------------------


# -------------------------------------------------------------- COMMENTS -----------------------------------------------------------------------------------------------# 
