from rest_framework import serializers
from .models import *

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['name', 'description', 'status', 'pk']
        

class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element

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