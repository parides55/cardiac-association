import os
import requests
from django.core.mail import send_mail, mail_admins
from django.conf import settings
from celery import shared_task
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .models import *


@shared_task(name="renew_member_annual_subscription")
def renew_member_annual_subscription():
    
    # Get all active members and find their credentials
    members = Member.objects.filter(membership_status = "active")
    
    for member in members:
        try:
            if member.next_payment_date == datetime.now().month:
                # Get the credentials for the member
                client_id = member.client_id
                credentials = get_credentials(client_id)
                make_a_payment(credentials)
        except Exception as e:
            print(f"Error retrieving credentials for member {member.id}: {e}")


def get_credentials(client_id):
    
    url = 'https://gateway-test.jcc.com.cy/payment/rest/getBindings.do'
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    
    data = {
        "userName": settings.JCC_API_USERNAME,
        "password": settings.JCC_API_PASSWORD,
        "clientId": client_id,
    }
    
    response = requests.post(url, data=data, headers=headers)
    response = response.json()
    
    try:
        if response.errorCode == 0:
            bindingId = response.get("bindings", {}).get("bindingId")
            return bindingId
    except Exception as e:
        print(f"Error retrieving binding ID: {e}")


def make_a_payment(bindingId):
    mail_admins(Subject="Payment Notification", message=f"Payment made for binding ID: {bindingId}")
