import os
from django.core.mail import send_mail
from celery import shared_task
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings
from .models import *

@shared_task
def charge_annual_subscription(member_id):
    
    today = datetime.now()
    
    member = Member.objects.get(id=member_id)
    member.last_payment_date = datetime.now()
    member.next_payment_date = today + relativedelta(years=1)
    member.is_paid = True
    member.save()
    return member.id


@shared_task(name='send_email_monthly')
def send_email_monthly():
    
    subject = "Monthly Newsletter"
    from_email = settings.EMAIL_HOST_USER
    members = Member.objects.filter(is_paid=True)
    
    for member in members:
        message = f"Dear {member.name},\n\nWe hope you are doing well. Here is our monthly newsletter. We hope you enjoy it.\n\nBest regards,\n\nThe Cardiac Association Team"
        send_mail(subject, message, from_email, [member.email])

    return f"Emails sent to {len(members)} members."