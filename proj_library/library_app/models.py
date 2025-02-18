from datetime import timedelta
from django.db import models
from django.db.models.functions import Now


# Create your models here.
class Genre(models.Model):
    genre = models.CharField(max_length=255)
    insert_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    activate = models.BooleanField(default=True)

    
class Loan(models.Model):

    class Status(models.IntegerChoices):
        AVAILABLE = 1, "Available"
        ON_LOAN = 2, "On Loan"
        LOST = 3, "Lost"
        DAMAGED = 4, "Damaged"

    user = models.IntegerField(unique = True)
    book = models.IntegerField(unique = True)
    status = models.IntegerField(choices = Status, default = Status.AVAILABLE)
    due_date = models.DateField(db_default = Now() + timedelta(days=30))
    insert_date = models.DateField(auto_now_add = True)
    update_date = models.DateField(auto_now = True)