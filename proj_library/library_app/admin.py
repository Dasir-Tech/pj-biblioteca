from django.contrib import admin
from .models import Genre,Author,Editor
#from .models import Nome_model, elenco dei model

# RICORDA -> MIGRARE I MODEL !!!!

# Register your models here.

'''
# PERSONALIZZARE il pannello Admin

admin.site.register(Nome_model)

class Nome_modelAdmin(admin.ModelAdmin):
    list_display = ("title","author","genre",)
    
admin.site.register(Nome_model, Nome_modelAdmin)    
'''

admin.site.site_header = "Gestion Library"
admin.site.site_title = "Admin - Library"
admin.site.index_title = "Admin Control Pannel"

'''
#nome_file.CSS per personalizzare la pag dell' Admin

class CustomAdmin(admin.AdminSite):
    def get_urls(self):
        return super().get_urls()
    
    class Media:
        css = {
            "all" : ("admin/css/custom.css",)
        }
        
admin.site = CustomAdmin()   
'''

class GenreAdmin(admin.ModelAdmin):
    list_display = ("genre", "insert_date", "update_date", "activate")
    actions = ['activate', 'deactivate']
    list_filter = ('activate',)
    search_fields = ('genre',)

    def activate(self, request, queryset):
        queryset.update(activate=True)

    def deactivate(self, request, queryset):
        queryset.update(activate=False)

admin.site.register(Genre, GenreAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name_author', 'insert_date', 'update_date', 'activate')
    list_filter = ('name_author', 'insert_date', 'update_date', 'activate') #filtri laterali
    actions = ['activate', 'deactivate']
    search_fields = ('name_author',)

    def activate(self, request, queryset):
        queryset.update(activate=True)

    def deactivate(self, request, queryset):
        queryset.update(activate=False)

admin.site.register(Author, AuthorAdmin)

class EditorAdmin(admin.ModelAdmin):
    list_display = ('editor', 'insert_date', 'update_date', 'activate')
    list_filter = ('activate',)
    search_fields = ('editor',)
    actions = ['activate', 'deactivate']

    def activate(self, request, queryset):
        queryset.update(activate=True)

    def deactivate(self, request, queryset):
        queryset.update(activate=False)

admin.site.register(Editor, EditorAdmin)
