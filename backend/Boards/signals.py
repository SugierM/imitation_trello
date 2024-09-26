from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from guardian.shortcuts import assign_perm, remove_perm
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

from .models import BoardMembership, ROLE_PERMISSIONS

User = get_user_model()

@receiver(post_save, sender=BoardMembership)
def assign_role_permissions(sender, instance, created, **kwargs):
    """
    Assigns permissions to a user based on their role within a board.
    Removes any existing permissions related to the board before assigning new ones.
    """
    user = instance.user
    board = instance.board
    role = instance.role.upper()

    # First, remove all existing permissions related to this board for the user
    for role_perms in ROLE_PERMISSIONS.values():
        for model, perms in role_perms.items():

            try:
                # Use lowercase app_label to match Django's default
                model_obj = apps.get_model('boards', model)
            except LookupError:
                continue

            # Get the ContentType for the model
            content_type = ContentType.objects.get_for_model(model_obj)

            for perm_codename in perms:
                # **Remove the app_label prefix**
                full_perm_codename = perm_codename
                remove_perm(full_perm_codename, user, board)

    # Assign new permissions based on the current role
    permissions = ROLE_PERMISSIONS.get(role, {})

    for model, perms in permissions.items():
        try:
            # Use lowercase app_label to match Django's default
            model_obj = apps.get_model('boards', model)
        except LookupError:
            continue 

        content_type = ContentType.objects.get_for_model(model_obj)

        for perm_codename in perms:
            # **Remove the app_label prefix**
            full_perm_codename = perm_codename
            print(f"Assigning permission: {full_perm_codename}")
            assign_perm(full_perm_codename, user, board)


@receiver(post_delete, sender=BoardMembership)
def remove_role_permissions_on_delete(sender, instance, **kwargs):
    """
    Removes all permissions from a user when their BoardMembership is deleted.
    """
    user = instance.user
    board = instance.board
    role = instance.role.upper()

    permissions = ROLE_PERMISSIONS.get(role, {})
    for model, perms in permissions.items():
        try:
            # Use lowercase app_label to match Django's default
            model_obj = apps.get_model('boards', model)
        except LookupError:
            continue

        content_type = ContentType.objects.get_for_model(model_obj)

        for perm_codename in perms:
            # **Remove the app_label prefix**
            full_perm_codename = perm_codename

            remove_perm(full_perm_codename, user, board)
