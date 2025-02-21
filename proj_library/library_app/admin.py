from datetime import timedelta
from django.contrib import admin

from django.utils.timezone import now
from .models import Loan, Author, Book, Genre, Editor, CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

class DateFilter(admin.SimpleListFilter):
    title = "Due Date"
    parameter_name = "select_date"

    def lookups(self, request, model_admin):
        return [
            ("exp","Expiring"),
            ("over", "Overdue"),
        ]
    def queryset(self, request, queryset):

        if self.value() == "exp":
            return (queryset.exclude(active=False).filter(
                due_date__gte = now().date() + timedelta(days=2)
            ).filter(status=2))
        elif self.value() == "over":
            return queryset.exclude(active=False).filter(
                due_date__lte = now().date()
            ).filter(status=2)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author', 'insert_date', 'update_date', 'activate')
    list_filter = ('author', 'insert_date', 'update_date', 'activate') #filtri laterali
    actions = ('activate_or_deactivate')
    def activate_or_deactivate(self, request, queryset): #cambia il boolean 'activate' in false
        attivati= queryset.filter(activate=False).queryset.update(activate=True)
        disattivati= queryset.filter(activate=True).queryset.update(activate=False)
=======
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

    def activate(self, request, queryset):
        queryset.update(activate=True)
    def deactivate(self, request, queryset):
        queryset.update(activate=False)

class GenreAdmin(admin.ModelAdmin):
    list_display = ("genre", "insert_date", "update_date", "activate")
    actions = ['activate', 'deactivate']
    list_filter = ('activate',)
    search_fields = ('genre',)

    def activate(self, request, queryset):
        queryset.update(activate=True)

    def deactivate(self, request, queryset):
        queryset.update(activate=False)
class CustomUserAdmin(UserAdmin):
    # Definizione dei campi personalizzati add user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informazioni Aggiuntive', {'fields': ('phone_number',  'email', 'first_name', 'last_name','is_active', 'is_staff')}),
    )

   #Definizione vista lista user
    list_display = ('username', 'email', 'phone_number',  'is_active', 'is_staff')

class Active(admin.SimpleListFilter):
    title = "Active"
    parameter_name = "select_active"

    def lookups(self, request, model_admin):
        return [
            ("act","Active"),
            ("dea","Deactive"),
        ]
    def queryset(self, request, queryset):
        if self.value() == "act":
            return queryset.exclude(active=False)
        elif self.value() == "dea":
            return queryset.exclude(active=True)

class Status(admin.SimpleListFilter):
    title = "Status"
    parameter_name = "select_status"

    def lookups(self, request, model_admin):
        return [
            ("1", "Available"),
            ("2", "On Loan"),
            ("3", "Lost"),
            ("4", "Damaged"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.exclude(active=False).filter(status=1)
        elif self.value() == "2":
            return queryset.exclude(active=False).filter(status=2)
        elif self.value() == "3":
            return queryset.exclude(active=False).filter(status=3)
        elif self.value() == "4":
            return queryset.exclude(active=False).filter(status=4)

class LoanAdmin(admin.ModelAdmin):
    list_display = ("id", "user_ID", "book_ID", "status", "due_date", "insert_date", "update_date", "active")
    list_filter = (DateFilter,Status ,Active)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(Book)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Editor, EditorAdmin)
