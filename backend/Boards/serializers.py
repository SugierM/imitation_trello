from rest_framework import serializers
from .models import *
from Users.serializers import UserLookupSerializer
from datetime import date
from Users.models import User
from rest_framework.reverse import reverse

# -------------------------------------------------------------- BOARDS ------------------------------------------------------------------------------------------------
class BoardBaseSerializer(serializers.ModelSerializer):
    creator = UserLookupSerializer()
    class Meta:
        model = Board
        fields = [
            "pk", 
            "name", 
            "description", 
            "status", 
            "creator",
        ] 

        read_only_fields = [
            "creator"
        ]


class BoardSerializer(BoardBaseSerializer):
    can_edit = serializers.SerializerMethodField()
    total_elements = serializers.IntegerField()
    completed_elements = serializers.IntegerField()
    first_element = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = BoardBaseSerializer.Meta.fields + [ 
            "can_edit", 
            "total_elements", 
            "completed_elements",
            "first_element"
        ]

        read_only_fields = BoardBaseSerializer.Meta.read_only_fields + [
            "can_edit",
            "total_elements", 
            "completed_elements",
            "first_element",
        ]
        
    def get_can_edit(self, obj):
        request = self.context.get("request")
        if request:
            edit_roles = ["ADMIN", "EDITOR"]
            return obj.memberships.filter(user=request.user, role__in=edit_roles).exists()
        
    def get_first_element(self, obj):
        element = obj.elements.exclude(due_date__isnull=True).order_by("-due_date").first()
        if element:
            return {
                "name": element.name,
                "due_date": element.due_date,
                "pk": element.pk
            }
        return None
    
        
    def validate_name(self, value):
        if len (value) < 4:
            raise serializers.ValidationError("Name must be at least 4 characters long") 

        user = self.context["request"].user 
        if Board.objects.filter(name=value, creator=user).exists():
            raise serializers.ValidationError("You have already created board with this name")
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
    board_creator = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = [
            "pk",
            "name",
            "status",
            "board_creator",
        ]

    def get_board_creator(self, obj):
        return obj.creator.get_full_name() if obj.creator else None

# -------------------------------------------------------------- ELEMENTS -----------------------------------------------------------------------------------------------

class ElementsBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = [
            "pk",
            "board", 
            "name", 
            "description", 
            "due_date", 
            "order", 
            "status",
        ]
        read_only_fields = [
            "pk",
            "board",
            ]
        
    def get_can_edit(self, obj):
        request = self.context.get("request")
        if request:
            edit_roles = ["ADMIN", "EDITOR"]
            return obj.board.memberships.filter(user=request.user, role__in=edit_roles).exists()

    def get_first_task(self, obj):
        task = obj.tasks.exclude(due_date__isnull=True).order_by("-due_date").first()
        if task:
            return {
                "name": task.name,
                "pk": task.pk,
                "due_date": task.due_date
            }
        return None


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

class ElementsSerializer(ElementsBaseSerializer):
    can_edit = serializers.SerializerMethodField()
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    first_task = serializers.SerializerMethodField()
    postponed_tasks = serializers.IntegerField()
    
    class Meta:
        model = Element
        fields = ElementsBaseSerializer.Meta.fields + [
            "can_edit",
            "total_tasks",
            "completed_tasks",
            "postponed_tasks",
            "first_task",
            ]
        
        read_only_fields = ElementsBaseSerializer.Meta.read_only_fields + [
            "first_task",
            "total_tasks",
            "completed_tasks",
            "postponed_tasks"
            ]
        


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
    class Meta:
        model = Task
        fields = ['element', 'name', 'description', 'due_date', 'priority',
                   'labels', 'status']
        
    def validate_name(self, value):
        element_id = self.initial_data.get("element")
        if element_id:
            element = Element.objects.get(id=element_id)
        else:
            raise serializers.ValidationError("This element doesn't exists.")
        
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

# ---------------------------------------------------------- BOARD MEMBERSHIPS -----------------------------------------------------------------------------------------

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
        return BoardBaseSerializer(boards, many=True, context=context).data


# -------------------------------------------------------------- COMMENTS ----------------------------------------------------------------------------------------------

class CommentSerializer(serializers.ModelSerializer):
    time_stamp = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            "author",
            "text",
            "time_stamp"
        ]

        read_only_fields = [
            "author",
            "time_stamp"
        ]


    def get_time_stamp(self, obj):
        return str(obj)


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "content_type",
            "object_id",
            "content_object",
            "text"
        ]

# ------------------------------------------------------------ ATTACHMENTS ----------------------------------------------------------------------------------------------

# Create, Retrieve or Delete
class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = [
            "file",
            "extension",
            "uploaded_at",
            "author",
        ]
        read_only_fields = [
            "extension",
            "author",
            "uploaded_at",
        ]
    
    def validate_file(self, value):
        allowed_extensions = ["png", "jpg", "jpeg", "pdf", "doc", "docx", "txt"]
        extension = value.name.split(".")[-1]
        if extension not in allowed_extensions:
            raise serializers.ValidationError(f"Files with extension '{extension}' are not allowed")
        
        self.context["validated_extension"] = extension
        return value
    

    def create(self, validated_data):
        validated_data['extension'] = self.context.get('validated_extension')
        return super().create(validated_data)


# Leave it for now
class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label





