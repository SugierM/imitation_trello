from django.db import models
# from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# from django.db.models.signals import post_save, m2m_changed
# from django.dispatch import receiver
# from guardian.shortcuts import assign_perm, remove_perm


class Board(models.Model):
    class Status(models.IntegerChoices):
        ONGOING = 0, 'Ongoing'
        DONE = 1, 'Done'

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_boards')
    status = models.IntegerField(choices=Status.choices, default=Status.ONGOING)


    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            BoardMembership.objects.create(board=self, user=self.creator, role=BoardMembership.Role.ADMIN)

    def __str__(self) -> str:
        return self.name


class Element(models.Model):
    class Status(models.IntegerChoices):
        ONGOING = 0, 'Ongoing'
        DONE = 1, 'Done'
        POSTPONED = 2, 'Postponed'

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='elements')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0) # Think about this one!
    status = models.IntegerField(choices=Status.choices, default=Status.ONGOING)

    def __str__(self) -> str:
        return self.name


class Label(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="labels", null=True, blank=True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7) # ( #0000FF ) for example
    is_global = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Task(models.Model):
    class Priority(models.IntegerChoices):
        LEAST_IMPORTANT = 0, 'Least Important'
        VERY_LOW = 1, 'Very Low'
        LOW = 2, 'Low'
        MEDIUM = 3, 'Medium'
        HIGH = 4, 'High'
        MOST_IMPORTANT = 5, 'Most Important'
    
    class Status(models.IntegerChoices):
        ONGOING = 0, 'Ongoing'
        DONE = 1, 'Done'
        POSTPONED = 2, 'Postponed'
         

    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    due_date = models.DateField(null=True, blank=True)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.LEAST_IMPORTANT)
    labels = models.ManyToManyField(Label, related_name='tasks', blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.ONGOING)

    class Meta:
        indexes = [
            models.Index(fields=['due_date']),
            models.Index(fields=['priority']),
        ]

    def clean(self):
        if self.due_date and self.element.due_date and self.due_date > self.element.due_date:
            raise ValidationError('Task due date cannot be after the element due date.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubTask(models.Model):
    class Status(models.IntegerChoices):
        ONGOING = 0, 'Ongoing'
        DONE = 1, 'Done'
        POSTPONED = 2, 'Postponed'
    name = models.CharField(max_length=100)
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    status = models.IntegerField(choices=Status.choices, default=Status.ONGOING)


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        date_format = "%Y-%m-%d %H:%M"
        if self.updated_at > self.created_at:
            end = f"updated on {self.updated_at.strftime(date_format)}."
        else:
            end = f"created on {self.created_at.strftime(date_format)}"
        return f'Comment by {self.user.get_full_name()} {end}'
    

class Attachment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    file = models.FileField(upload_to="attachments/")
    extension = models.CharField(max_length=10, blank=True, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Activity(models.Model):
    board = models.ForeignKey(Board, related_name='activity', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"


class BoardMembership(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        EDITOR = 'EDITOR', 'Editor'
        MEMBER = 'MEMBER', 'Member'
        VISITOR = 'VISITOR', 'Visitor'

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='board_memberships')
    role = models.CharField(max_length=10, choices=Role.choices)

    class Meta:
        unique_together = ('board', 'user')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()} on {self.board.name}"


ROLE_PERMISSIONS = {
    'ADMIN': {
        'Board': ['change_board', 'delete_board', 'view_board'],
        'Element': ['add_element', 'change_element', 'delete_element', 'view_element'],
        'Task': ['add_task', 'change_task', 'delete_task', 'view_task'],
        'SubTask': ['add_subtask', 'change_subtask', 'delete_subtask', 'view_subtask'],
        'Comment': ['add_comment', 'change_comment', 'delete_comment', 'view_comment'],
        'Attachment': ['add_attachment', 'delete_attachment', 'view_attachment'],
        'Activity': ['view_activity'],
    },
    'EDITOR': {
        'Board': ['change_board', 'view_board'],
        'Element': ['add_element', 'change_element', 'view_element'],
        'Task': ['add_task', 'change_task', 'view_task'],
        'SubTask': ['add_subtask', 'change_subtask', 'view_subtask'],
        'Comment': ['add_comment', 'change_comment', 'view_comment'],
        'Attachment': ['add_attachment', 'view_attachment', 'delete_attachment'],
        'Activity': ['view_activity'],
    },
    'MEMBER': {
        'Board': ['view_board'],
        'Element': ['view_element'],
        'Task': ['change_task', 'view_task'],
        'SubTask': ['change_subtask', 'view_subtask'],
        'Comment': ['add_comment', 'change_comment', 'view_comment'],
        'Attachment': ['add_attachment', 'view_attachment'],
        'Activity': ['view_activity'],
    },
    'VISITOR': {
        'Board': ['view_board'],
        'Element': ['view_element'],
        'Task': ['view_task'],
        'SubTask': ['view_subtask'],
        'Comment': [],
        'Attachment': [],
        'Activity': [],
    },
}