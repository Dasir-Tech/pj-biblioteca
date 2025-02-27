from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from proj_library.library_app.models import Loan

class Command(BaseCommand):
    help = 'Invia email di promemoria prima della scadenza'
    def handle(self, *args, **kwargs):
        loans = Loan.objects.filter(
                due_date__gte = now().date()).filter(due_date__lte = now().date() + timedelta(days=2)
            ).filter(status=2)
        for loan in loans:
            emails = Loan.select_related("user").values_list("user__email", flat=True)
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
            self.stdout.write(self.style.SUCCESS(f'Email inviata a {loan.email}"'))