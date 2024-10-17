from django.contrib import admin

from .models import Board, Element, Task, Comment, Activity, Attachment, SubTask, BoardMembership, Label

admin.site.register([Board, Element, Task, Comment, Activity, Attachment, SubTask, BoardMembership])

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'is_global', 'board')
    list_filter = ('is_global', 'board')
    search_fields = ('name',)