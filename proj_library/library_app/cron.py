from datetime import timedelta
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Loan

def auto_email():
    loans = Loan.objects.filter(
        due_date__gte=now().date()).filter(due_date__lte=now().date() + timedelta(days=2)).filter(status=2)
    for loan in loans:
        email = loan.select_related("user").values_list("user__email", flat=True)
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