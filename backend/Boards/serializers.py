from rest_framework import serializers
from .models import *
from Users.serializers import UserLookupSerializer

class BoardSerializer(serializers.ModelSerializer):
    creator = UserLookupSerializer()
    class Meta:
        model = Board
        fields = ['name', 'description', 'status', "creator"]


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ["board_url", "name", "description", "due_date", "order", "status"]

    def get_board_ulr():
        pass

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['element', 'name', 'description', 'due_date', 'priority',
                   'labels', 'status']

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment

class BoardMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMembership
        fields = [
            "board",
            "user",
            "role",
        ]

    @staticmethod
    def get_common_boards(user1, user2, context=None):
        common_boards_ids = BoardMembership.objects.filter(user=user1).filter(
            board__memberships__user=user2
            ).values_list("board", flat=True).distinct()
        
        boards = Board.objects.filter(id__in=common_boards_ids)
        return BoardSerializer(boards, many=True, context=context).data

