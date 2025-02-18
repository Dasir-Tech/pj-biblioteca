from django.contrib import admin
from .models import Editor


class EditorAdmin(admin.ModelAdmin):
    list_display = ('editor', 'insert_date', 'update_date', 'activate')
    list_filter = ('activate',)
    search_fields = ('editor',)
    
    def activate(self, request, queryset): 
        queryset.update(activate=True)
    def deactivate(self, request, queryset): 
        queryset.update(activate=False)

admin.site.register(Editor, EditorAdmin)
