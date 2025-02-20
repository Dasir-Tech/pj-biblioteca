from datetime import timedelta
from django.contrib import admin
from django.utils.timezone import now
from .models import Loan

class DateFilter(admin.SimpleListFilter):
    title = "Due Date"
    parameter_name = "select_date"


    def lookups(self, request, model_admin):
        return [
            ("ong", "Ongoing"),
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