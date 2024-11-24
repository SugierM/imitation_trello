from rest_framework.permissions import BasePermission
from .models import *

class IsRoleAuthorized(BasePermission):
    def has_permission(self, request, view):
        model_name = self.get_model_name(view)
        if request.method == "POST" and model_name == "board":
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        board = self.get_board_from_object(obj)
        if not board:
            return False

        try:
            membership = BoardMembership.objects.get(user=user, board=board)
        except BoardMembership.DoesNotExist:
            return False

        user_role = membership.role
        resource = obj.__class__.__name__
        
        action = self.get_action(request.method, view)
        allowed_actions = ROLE_PERMISSIONS.get(user_role, {}).get(resource, [])
        return action in allowed_actions

    def get_board_from_object(self, obj):
        if isinstance(obj, Board):
            return obj
        elif isinstance(obj, Element):
            return obj.board
        elif isinstance(obj, Task):
            return obj.element.board
        elif isinstance(obj, SubTask):
            return obj.task.element.board
        elif isinstance(obj, Comment):
            return obj.task.element.board
        elif isinstance(obj, Attachment):
            return obj.task.element.board
        elif isinstance(obj, Activity):
            return obj.board
        else:
            return None

    def get_action(self, method, view):
        model_name = self.get_model_name(view)
        if method == 'GET':
            return 'view_' + model_name
        elif method == 'POST':
            return 'add_' + model_name
        elif method in ['PUT', 'PATCH']:
            return 'change_' + model_name
        elif method == 'DELETE':
            return 'delete_' + model_name
        return None
    

    def get_model_name(self, view):
        if hasattr(view, 'queryset') and view.queryset is not None:
            return view.queryset.model.__name__.lower()
        return view.__class__.__name__.lower()
    

class TaskAssignedOrRoleAuthorized(IsRoleAuthorized):
    def has_object_permission(self, request, view, obj):
        user = request.user

        # if obj.__class__.__name__ == "Task" and request.method in ["PUT", "PATCH"]:
        #     return obj.assigned == user

        board = self.get_board_from_object(obj)
        if not board:
            return False
        
        try:
            membership = BoardMembership.objects.get(user=user, board=board)
        except BoardMembership.DoesNotExist:
            return False

        user_role = membership.role
        resource = obj.__class__.__name__

        action = self.get_action(request.method, view)
        allowed_actions = ROLE_PERMISSIONS.get(user_role, {}).get(resource, [])
        return action in allowed_actions