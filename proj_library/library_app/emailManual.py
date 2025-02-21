from datetime import timedelta
#from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Loan

user = Loan.objects.select_related('user_ID').all

for u in user:
    print(u)

'''
def expiration_email(user,loan):
    user_email = user.email
    user_name = user.name
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
'''
