from django.db import models

# Create your models here.
class Genre(models.Model):
    genre = models.CharField(max_length=255)
    insert_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    activate = models.BooleanField(default=True)