from django.db import models
from django.db.models.functions import Now


# Create your models here.
class Author(models.Model):
            name_author = models.CharField(max_length=255)
            insert_date = models.DateField(auto_now_add=True)
            update_date = models.DateField(auto_now=True)
            activate = models.BooleanField(default=True)


