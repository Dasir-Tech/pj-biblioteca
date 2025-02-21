'''
from datetime import timedelta
from django.core.mail import send_mail
from django.utils.timezone import now, activate
#from library_app.models import Loan
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Sends expiration notice email"

    #console output
    def handle(self, *args, **options):
        date = now().date() + timedelta(days=2)
        loans = Loan.objects.filter(due_date = date, active = True, status = Loan.Status.ON_LOAN)
        user_ID = None

        try:
            loan = Loan.objects.get(id=Loan.id)
            user_ID = loan.user_ID
            print(f"{user_ID}")

        except Loan.DoesNotExist:
            self.stdout.write(f"Loan does not exists")





    
    
    def expiration_email(loan):
        user_email = 'User.email???'
        user_name = "User.name"
        due_date = loan.due_date
        try:
            send_mail(
                "Expiration notice from Neighborhood Library",
                f"Hello {user_name}!\n"
                f"The expiration date of your loan is: {due_date}.\n"
                f"We kindly remind you to return the book you have loaned.\n"
                f"Thanks for your collaboration, see you in Neighborhood Libray ;)",
                "laura.comparelli@dasir.it",
                [f"{user_email}"],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending expiration notice to {user_email}: {e}")
    
    #Invio automatico di Avviso scadenza
    def auto_expiration_notice(due_date,user_email):
        try:
            date_now = now().date()
            date_diff = due_date - date_now
            if date_diff.days == 2:
                expiration_email(user_email)
            else:
                pass
        except Exception as e:
            print(f"Errore nell'invio dell'avviso di scadenza: {e}")
    
    
    auto_expiration_notice(loan.due_date,'User.email???')
'''