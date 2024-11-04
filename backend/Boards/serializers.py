from rest_framework import serializers
from .models import *
from Users.serializers import UserLookupSerializer
from datetime import date
from Users.models import User

# -------------------------------------------------------------- BOARDS ------------------------------------------------------------------------------------------------

class BoardSerializer(serializers.ModelSerializer):
    creator = UserLookupSerializer()
    class Meta:
        model = Board
        fields = ['name', 'description', 'status', "creator"]

        extra_kwargs = {
            "creator": {"read_only": True}
        }

    def validate_name(self, value):
        if len (value) < 4:
            raise serializers.ValidationError({"name": "Name must be at least 4 characters long"}) 

        user = self.context["request"].user 
        if Board.objects.filter(name=value, creator=user).exists():
            raise serializers.ValidationError({"name": "You have already created board with this name"})
        return value
    
        
class BoardCreateSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = [
            "name",
            "description",
        ]

    def create(self, validated_data):
        name = validated_data.get("name")
        user = self.context["request"].user
        if Board.objects.filter(name=name, creator=user).exists():
            raise serializers.ValidationError({"name": "You have already created board with this name"})
        
        validated_data["creator"] = user
        if len (validated_data.get("name", None)) < 4:
            raise serializers.ValidationError({"name": "Name must be at least 4 characters long"})
        board = Board.objects.create(**validated_data)
        return board


class BoardsListSerializer(serializers.ModelSerializer):
    board_url = serializers.HyperlinkedIdentityField(
        view_name = "board-detail",
        lookup_field = "pk",
    )

    board_creator = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            "name",
            "status",
            "board_url",
            "board_creator" 
        ]

    def get_board_creator(self, obj):
        return obj.creator.get_full_name() if obj.creator else None

# -------------------------------------------------------------- ELEMENTS -----------------------------------------------------------------------------------------------

class ElementSerializer(serializers.ModelSerializer):
    board_url = serializers.HyperlinkedIdentityField(
        view_name = "board-detail",
        lookup_field = "board_id",
        lookup_url_kwarg = "pk"
    )
    class Meta:
        model = Element
        fields = ["board_url", "board", "name", "description", "due_date", "order", "status"]

    def validate_due_date(self, value):
        if value is None:
            pass
        elif value < date.today():
            raise serializers.ValidationError("Due date must be in the future")
        return value
    

    def validate_name(self, value):
        board_id = self.initial_data.get("board")
        if board_id:
            board = Board.objects.get(id=board_id)
        else:
            raise serializers.ValidationError("This board doesn't exist")
        
        if Element.objects.filter(board=board, name=value).exists():
            raise serializers.ValidationError("An element with this name already exists within this board.")
        
        return value

    

class ElementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = [
            "board",
            "name",
            "description",
            "due_date",
            "order",
        ]

    def validate_due_date(self, value):
        if value is None:
            pass
        elif value < date.today():
            raise serializers.ValidationError("Due date must be in the future")
        return value
    

    def validate_name(self, value):
        board_id = self.initial_data.get("board")
        if board_id:
            board = Board.objects.get(id=board_id)
        else:
            raise serializers.ValidationError("This board doesn't exist")
        
        if Element.objects.filter(board=board, name=value).exists():
            raise serializers.ValidationError("An element with this name already exists within this board.")
        
        return value

# -------------------------------------------------------------- TASKS ------------------------------------------------------------------------------------------------

class TaskSerializer(serializers.ModelSerializer):
    element_url = serializers.HyperlinkedIdentityField(
        view_name='element-detail',
        lookup_field='element_id',
        lookup_url_kwarg='pk',
    )
    class Meta:
        model = Task
        fields = ['element_url', 'element', 'name', 'description', 'due_date', 'priority',
                   'labels', 'status']
        
    def validate_name(self, value):
        element_id = self.initial_data.get("element")
        if element_id:
            element = Element.objects.get(id=element_id)
        else:
            raise serializers.ValidationError("This element does't exists.")
        
        if Task.objects.filter(element=element, name=value).exists():
            raise serializers.ValidationError("Task with this name already exists within this element.")

        return value

    def validate_due_date(self, value):
        if value is None:
            pass
        elif value < date.today():
            raise serializers.ValidationError("Due date must be in the future")
        return value


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['element', 'name', 'description', 'due_date', 'priority',
                   'labels', 'status']

    def validate_name(self, value):
        element_id = self.initial_data.get("element")
        if element_id:
            element = Element.objects.get(id=element_id)
        else:
            raise serializers.ValidationError("This element does't exists.")
        
        if Task.objects.filter(element=element, name=value).exists():
            raise serializers.ValidationError("Task with this name already exists within this element.")

        return value
    
    def validate_due_date(self, value):
        if value is None:
            pass
        elif value < date.today():
            raise serializers.ValidationError("Due date must be in the future")
        return value

# -------------------------------------------------------------- SUBTASKS ----------------------------------------------------------------------------------------------

# -------------------------------------------------------------- BOARDS ------------------------------------------------------------------------------------------------


# Leave it for now
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

