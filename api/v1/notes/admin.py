from django.contrib import admin

from api.v1.notes.models import Note


# Register your models here.

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description', 'date']