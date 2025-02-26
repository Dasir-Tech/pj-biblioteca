'''
from django.core.mail import send_mail
from datetime import datetime
import schedule
import time
from .models import Loan

def send_due_date_notification():
    due_date = Loan.objects.values("due_date")

    if (due_date - datetime.now()).days <= 2:
        emails = Loan.objects.select_related("user").values_list("user__email", flat=True)
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

schedule.every().day.at("16:07").do(send_due_date_notification)

while True:
    schedule.run_pending()
    time.sleep(1)
'''