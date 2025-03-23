from celery import shared_task
from datetime import datetime
from dateutil.relativedelta import relativedelta
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