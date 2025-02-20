from datetime import timedelta
from django.contrib import admin
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


admin.site.register(Loan, LoanAdmin)