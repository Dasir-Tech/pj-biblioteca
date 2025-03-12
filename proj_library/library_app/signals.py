from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Loan, Book

@receiver(post_save, sender=Loan)
def aggiorna_quantita_libro(sender, instance, **kwargs):
    if instance.status >= 2:
        libro = instance.book
        libro.qty -= 1
        libro.save()
    elif instance.status == 1 and instance.update_date:
        libro = instance.book
        libro.qty += 1
        libro.save()