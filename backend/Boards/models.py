from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

class Board(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_boards')

    def __str__(self) -> str:
        return self.name


class Element(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='elements')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7) # ( #0000FF ) for example


class Task(models.Model):
    class Priority(models.IntegerChoices):
        LEAST_IMPORTANT = 0, 'Least Important'
        VERY_LOW = 1, 'Very Low'
        LOW = 2, 'Low'
        MEDIUM = 3, 'Medium'
        HIGH = 4, 'High'
        MOST_IMPORTANT = 5, 'Most Important'

    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    due_date = models.DateField(null=True, blank=True)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.LEAST_IMPORTANT)
    labels = models.ManyToManyField(Label, related_name='label', blank=True)

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
    name = models.CharField(max_length=100)
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    task = models.ForeignKey(Task, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Activity(models.Model):
    board = models.ForeignKey(Board, related_name='activity', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    