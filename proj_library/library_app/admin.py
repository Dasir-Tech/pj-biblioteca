from datetime import timedelta
from django.contrib import admin
from django.utils.timezone import now
from .models import Loan

class DateFilter(admin.SimpleListFilter):
    title = "Date"
    parameter_name = "select_date"

    def lookups(self, request, model_admin):
        return [
            ("exp","Expiring"),
            ("over","Overdue" ),
        ]

    def queryset(self, request, queryset):

        if self.value() == "exp":
            return queryset.filter(
                due_date = now().date() + timedelta(days=2)
            )
        elif self.value() == "over":
            return queryset.exclude(due_date=now().date() - timedelta(days=1))


class LoanAdmin(admin.ModelAdmin):
    list_display = ("id","user_ID","book_ID","status","due_date","insert_date","update_date","active")
    list_filter = ("active",DateFilter)

admin.site.register(Loan, LoanAdmin)

'''
admin.site.site_header = "Gestion Library"
admin.site.site_title = "Admin - Library"
admin.site.index_title = "Admin Control Pannel"


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