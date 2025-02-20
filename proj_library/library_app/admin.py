from datetime import timedelta
from django.contrib import admin
from django.utils.timezone import now
from .models import Loan
from .models import Editor
from .models import Genre
from .models import Book
from django.utils.translation.trans_null import activate
from .models import Author

class DateFilter(admin.SimpleListFilter):
    title = "Date"
    parameter_name = "select_date"

    def lookups(self, request, model_admin):
        return [
            ("ong", "Ongoing"),
            ("exp","Expiring"),
        ]

    def queryset(self, request, queryset):
      
class EditorAdmin(admin.ModelAdmin):
    list_display = ('editor', 'insert_date', 'update_date', 'activate')
    list_filter = ('activate',)
    search_fields = ('editor',)

    def activate(self, request, queryset):
        queryset.update(activate=True)
    def deactivate(self, request, queryset):
        queryset.update(activate=False)

admin.site.register(Editor, EditorAdmin)

# Register your models here.
#Modificare modello in admin
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author', 'insert_date', 'update_date', 'activate')
    list_filter = ('author', 'insert_date', 'update_date', 'activate') #filtri laterali
    actions = ('activate_or_deactivate')
    def activate_or_deactivate(self, request, queryset): #cambia il boolean 'activate' in false
        attivati= queryset.filter(activate=False).queryset.update(activate=True)
        disattivati= queryset.filter(activate=True).queryset.update(activate=False)

admin.site.register(Author, AuthorAdmin)

class LoanAdmin(admin.ModelAdmin):
    list_display = ("id","user_ID","book_ID","status","due_date","insert_date","update_date","active")
    list_filter = ("active",DateFilter)

admin.site.register(Loan, LoanAdmin)

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
admin.site.register(Book)