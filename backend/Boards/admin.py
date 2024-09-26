from django.contrib import admin

from .models import Board, Element, Task, Comment, Activity, Attachment, SubTask

admin.site.register([Board, Element, Task, Comment, Activity, Attachment, SubTask])
