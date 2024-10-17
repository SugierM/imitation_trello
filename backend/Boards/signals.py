from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from guardian.shortcuts import assign_perm, remove_perm
from .models import BoardMembership, ROLE_PERMISSIONS

@receiver(post_save, sender=BoardMembership)
def assign_role_permissions(sender, instance, created, **kwargs):
    user = instance.user
    board = instance.board
    role = instance.role.upper()

    # Remove existing permissions
    for perms in ROLE_PERMISSIONS.values():
        for perm_codename in perms.get('Board', []):
            remove_perm(perm_codename, user, board)

    # Assign new permissions based on the current role
    permissions = ROLE_PERMISSIONS.get(role, {}).get('Board', [])
    for perm_codename in permissions:
        assign_perm(perm_codename, user, board)

@receiver(post_delete, sender=BoardMembership)
def remove_role_permissions_on_delete(sender, instance, **kwargs):
    user = instance.user
    board = instance.board
    role = instance.role.upper()

    permissions = ROLE_PERMISSIONS.get(role, {}).get('Board', [])
    for perm_codename in permissions:
        remove_perm(perm_codename, user, board)
