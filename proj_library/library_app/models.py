from django.db import models

class Editor(models.Model):
    editor = models.CharField(max_length=100)
    insert_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True) # Campo per disattivare senza cancellare

    def __str__(self):
        return self.editor
# Create your models here.

