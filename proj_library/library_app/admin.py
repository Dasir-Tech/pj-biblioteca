from datetime import timedelta
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Loan, Author, Book, Genre, Editor, CustomUser, New
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html


admin.site.index_title = "Dashboard" #titolo pagina admin


#BOOK
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author', 'insert_date', 'update_date', 'activate')
    list_filter = ('author', 'insert_date', 'update_date', 'activate') #filtri laterali
    search_fields = ('author',)
    actions = ['activate', 'deactivate']
    add_form_template = "admin/author_form.html"
    change_form_template = "admin/author_form.html"

    def activate(self, request, queryset):
        queryset.update(activate=True)

    def deactivate(self, request, queryset):
        queryset.update(activate=False)

class GenreAdmin(admin.ModelAdmin):
    list_display = ("genre", "insert_date", "update_date", "activate")
    actions = ['activate', 'deactivate']
    list_filter = ('activate',)
    search_fields = ('genre',)
    add_form_template = "admin/genre_form.html"
    change_form_template = "admin/genre_form.html"

    def activate(self, request, queryset):
        queryset.update(activate=True)

    def deactivate(self, request, queryset):
        queryset.update(activate=False)

class EditorAdmin(admin.ModelAdmin):
    list_display = ('editor', 'insert_date', 'update_date', 'activate')
    actions = ['activate', 'deactivate']
    list_filter = ('activate',)
    search_fields = ('editor',)
    add_form_template = "admin/editor_form.html"
    change_form_template = "admin/editor_form.html"

    def activate(self, request, queryset):
        queryset.update(activate=True)

    def deactivate(self, request, queryset):
        queryset.update(activate=False)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'display_author', 'display_genre', 'editor', 'isbn', 'qty', 'insert_date','update_date','activate')
    list_filter = ('activate',)
    search_fields = ('title', 'isbn')
    actions = ['activate', 'deactivate']

    add_form_template = "admin/book_form.html"
    change_form_template = "admin/book_form.html"

    def image_preview(self, obj):
        if obj.img:  # Controlla se l'immagine è presente
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;"/>',
                               obj.img.url)

    image_preview.short_description = 'Preview'

    def activate(self, request, queryset):
        queryset.update(activate=True)

    def deactivate(self, request, queryset):
        queryset.update(activate=False)

#USER
class CustomUserAdmin(UserAdmin):
    # Definizione dei campi personalizzati add user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informazioni Aggiuntive', {'fields': ('phone_number',  'email', 'first_name', 'last_name','is_active')}),
    )
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "is_active":
            formfield.label = ("Active")
        return formfield

    add_form_template = "admin/user_form.html"
    change_form_template = "admin/user_form.html"

   #Definizione vista lista user
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Gli utenti admin e bookseller vedono tutti gli utenti
        if request.user.is_superuser or \
           request.user.groups.filter(name__in=["admin", "bookseller"]).exists():
            return qs
        # Gli utenti "user" vedono solo se stessi
        elif request.user.groups.filter(name="user").exists():
            return qs.filter(id=request.user.id)
        return qs.none()

    def get_fieldsets(self, request, obj=None):
        fs = super().get_fieldsets(request, obj)

        if request.user.is_superuser or request.user.groups.filter(name__in=["admin", "bookseller"]).exists():
            return fs

        elif request.user.groups.filter(name="user").exists():

            new_fs = []
            for fieldset in fs:
                title, field_options = fieldset
                fields = field_options.get("fields", ())
                filtered_fields = tuple(f for f in fields if f not in ("groups", "user_permissions","is_active", "is_staff", "is_superuser", "last_login", "date_joined", "id_password_helptext",))

                if filtered_fields:
                    new_fs.append((title, {"fields": filtered_fields}))

            return new_fs

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name="user").exists():
            return False  # Gli utenti nel gruppo "user" non possono eliminare utenti
        return super().has_delete_permission(request, obj)

    list_display = ('username', 'email', 'phone_number',  'is_active', 'is_staff')
    search_fields = ('first_name','email',)
    list_filter = ('username', 'email', 'phone_number',  'is_active', 'is_staff')

#LOAN
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
                due_date__gte = now().date()).filter(due_date__lte = now().date() + timedelta(days=2)
            ).filter(status=2)).order_by('due_date')
        elif self.value() == "over":
            return queryset.exclude(active=False).filter(
                due_date__lte = now().date()
            ).filter(status=2).order_by('due_date')

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
            return queryset.exclude(active=False).filter(status=1).order_by('due_date')
        elif self.value() == "2":
            return queryset.exclude(active=False).filter(status=2).order_by('due_date')
        elif self.value() == "3":
            return queryset.exclude(active=False).filter(status=3).order_by('due_date')
        elif self.value() == "4":
            return queryset.exclude(active=False).filter(status=4).order_by('due_date')

class LoanAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "status", "due_date", "insert_date", "update_date", "active")
    list_filter = (DateFilter,Status ,Active)
    search_fields = ('id','book__title')
    actions = ['sendEmail','activate', 'deactivate']
    add_form_template = "admin/loan_form.html"
    change_form_template = "admin/loan_form.html"

    def activate(self, request, queryset):
        queryset.update(active=True)

    def deactivate(self, request, queryset):
        queryset.update(active=False)

    @admin.action(description="Send expired loan email")
    def sendEmail(self, request, queryset):
        emails = queryset.select_related("user").values_list("user__email", flat=True)
        for email in emails:
            send_mail(
                "Expiration notice from Neighborhood Library",
                f"--------------------------------\n"
                f"Hello!\n"
                f"We kindly remind you to return the book you have loaned.\n"
                f"Thanks for your collaboration, see you in Neighborhood Libray ;)\n"
                f"--------------------------------\n",
                "laura.comparelli@dasir.it",
                [email],
                fail_silently=False,
            )

class NewAdmin(admin.ModelAdmin):
    list_display = ('img', 'header', 'text', 'activate',  'insert_date', 'update_date')
    list_filter = ('header', 'activate')
    search_fields = ('header', 'text')
    add_form_template = "admin/new_form.html"
    change_form_template = "admin/new_form.html"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Gli utenti admin e bookseller vedono tutti gli utenti
        if request.user.is_superuser or \
                request.user.groups.filter(name__in=["admin", "bookseller"]).exists():
            return qs
        # Gli utenti "user" vedono solo se stessi
        elif request.user.groups.filter(name="user").exists():
            return qs.filter(user_ID_id=request.user.id)
        return qs.none()



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Editor, EditorAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(New, NewAdmin)