from datetime import timedelta, date
from django.db import models
from django.utils.timezone import now
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Author(models.Model):
    author = models.CharField(max_length=255)
    insert_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    activate = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return self.author

class Genre(models.Model):
    genre = models.CharField(max_length=255)
    insert_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    activate = models.BooleanField(default=True)

    def __str__(self):
        return self.genre

class Editor(models.Model):
    editor = models.CharField(max_length=100)
    insert_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    activate = models.BooleanField(default=True) # Campo per disattivare senza cancellare

    def __str__(self):
        return self.editor


class Book(models.Model):
    img = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(Author, help_text="Select one or more author for this book", null=False)
    genre = models.ManyToManyField(Genre, help_text="Select one or more genre for this book", null=False)
    editor = models.ForeignKey(Editor, help_text="Select an editor", null=False, on_delete=models.CASCADE)
    isbn = models.CharField('ISBN', max_length=13,
        unique=True,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
            '">ISBN number</a>')
    publication_date = models.DateField(null=False)
    qty = models.IntegerField(null=False)
    activate = models.BooleanField(default=True)
    insert_date = models.DateField(default=date.today(), null=False)
    update_date = models.DateField(auto_now=True, null=True)

    def display_author(self):
        return ', '.join(author.author for author in self.author.all()[:3])

    display_author.short_description = 'Author'

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def display_editor(self):
        return self.editor.editor

    display_editor.short_description = "Editor"

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)                  # Per disattivazione utenti

    def __str__(self):
        return self.username

class Loan(models.Model):

    class Status(models.IntegerChoices):
        AVAILABLE = 1, "Available"
        ON_LOAN = 2, "On Loan"
        LOST = 3, "Lost"
        DAMAGED = 4, "Damaged"

    #automatic due_date
    def AutoDueDate(self):
        return now().date() + timedelta(days=30)

    user_ID = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book_ID = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.IntegerField(choices = Status, default = Status.AVAILABLE)
    due_date = models.DateField(default=AutoDueDate)
    insert_date = models.DateField(auto_now_add = True)
    update_date = models.DateField(auto_now = True)
    active = models.BooleanField(default=True)
