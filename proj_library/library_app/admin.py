from django.contrib import admin
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