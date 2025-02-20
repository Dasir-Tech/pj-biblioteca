from django.contrib import admin
from .models import Editor


class EditorAdmin(admin.ModelAdmin):
    list_display = ('editor', 'insert_date', 'update_date', 'activate')
    list_filter = ('activate',)
    search_fields = ('editor',)

admin.site.register(Editor, EditorAdmin)
