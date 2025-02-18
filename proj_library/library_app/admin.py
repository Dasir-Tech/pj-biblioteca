from django.contrib import admin
from .models import Editor


class EditorAdmin(admin.ModelAdmin):
    list_display = ('editor', 'insert_date', 'update_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('editor',)

admin.site.register(Editor, EditorAdmin)
