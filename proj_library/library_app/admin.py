from datetime import timedelta
from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.utils.timezone import now
from .models import Loan

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
            return queryset.exclude(active=False).filter(
                due_date__gte = now().date() + timedelta(days=2)
            ).filter(status=2)
        elif self.value() == "over":
            return queryset.exclude(active=False).filter(
                due_date__lte = now().date()
            ).filter(status=2)

class EditorAdmin(admin.ModelAdmin):
    list_display = ('editor', 'insert_date', 'update_date', 'activate')
    list_filter = ('activate',)
    search_fields = ('editor',)

    def activate(self, request, queryset):
        queryset.update(activate=True)
    def deactivate(self, request, queryset):
        queryset.update(activate=False)

class LoanAdmin(admin.ModelAdmin):
    list_display = ("id","user_ID","book_ID","status","due_date","insert_date","update_date","active")
    list_filter = ("active",DateFilter)

class CustomUserAdmin(UserAdmin):
    # Definizione dei campi personalizzati add user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informazioni Aggiuntive', {'fields': ('phone_number',  'email', 'first_name', 'last_name','is_active', 'is_staff')}),
    )

   #Definizione vista lista user
    list_display = ('username', 'email', 'phone_number',  'is_active', 'is_staff')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Loan, LoanAdmin)
