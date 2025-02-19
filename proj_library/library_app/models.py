from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from datetime import date
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(Author, help_text="Select one or more author for this book", null=False)
    genre = models.ManyToManyField(Genre, help_text="Select one or more genre for this book", null=False)
    editor = models.ForeignKey(Editor, help_text="Select an editor for this book", null=False)
    isbn = models.CharField('ISBN', max_length=13,
        unique=True,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
            '">ISBN number</a>')
    publication_date = models.DateField(null=False)
    qty = models.IntegerField(null=False)
    activate = models.BooleanField(default=True)
    insert_date = models.DateField(default=date.now(), null=False)
    update_date = models.DateField(null=False)

    def display_author(self):
        return ', '.join(author.first_name + ' ' + author.last_name for author in self.author.all()[:3])

    display_author.short_description = 'Author'

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def display_editor(self):
        return self.editor.editor

    display_editor.short_description = "Editor"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])