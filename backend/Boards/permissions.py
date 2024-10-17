from rest_framework.permissions import BasePermission
from .models import *

class IsRoleAuthorized(BasePermission):
    def has_permission(self, request, view):
        if view.action == "create" and view.basename == 'board':
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
        
        action = self.get_action(view)
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

    def get_action(self, view):
        if view.action in ['list', 'retrieve']:
            return 'view_' + view.basename
        elif view.action == 'create':
            return 'add_' + view.basename
        elif view.action in ['update', 'partial_update']:
            return 'change_' + view.basename
        elif view.action == 'destroy':
            return 'delete_' + view.basename
        return None