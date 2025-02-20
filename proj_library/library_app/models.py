from datetime import timedelta
from django.db import models
from django.utils.timezone import now

class Loan(models.Model):

    class Status(models.IntegerChoices):
        AVAILABLE = 1, "Available"
        ON_LOAN = 2, "On Loan"
        LOST = 3, "Lost"
        DAMAGED = 4, "Damaged"

    #automatic due_date
    def AutoDueDate():
        return now().date() + timedelta(days=30)

    user_ID = models.ForeignKey(db_index = True)
    book_ID = models.ForeignKey(db_index = True)
    status = models.IntegerField(choices = Status, default = Status.AVAILABLE)
    due_date = models.DateField(default=AutoDueDate)
    insert_date = models.DateField(auto_now_add = True)
    update_date = models.DateField(auto_now = True)
    active = models.BooleanField(default=True)
