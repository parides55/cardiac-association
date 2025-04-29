import requests
from background_task import background
from django.core.mail import mail_admins
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.conf import settings
from .models import *


@background(schedule=60)
def check_member_for_renewal():
    
    today = timezone.localdate()
    
    members_for_renewal = Member.objects.annotate(
        next_payment_date_only=TruncDate('next_payment_date')).filter(
        membership_status="active",
        next_payment_date_only=today
    )
    
    if not members_for_renewal.exists():
        subject = "No members for renewal"
        text_content = "There are no members for renewal today."
        mail_admins(subject, text_content)
    else:
        for member in members_for_renewal:
            member_client_id = member.client_id
            
            store_credentials = get_credentials(member_client_id)
        
            subject = "Membership Expiry Reminder"
            
            text_content = f""""
            The store credentials for {member.name} {member.surname} are as follows:
            
            Client ID: {member_client_id}
            
            Binding ID: {store_credentials}
            
            """           

            mail_admins(subject, text_content)

def get_credentials(client_id):

    url = "https://gateway-test.jcc.com.cy/payment/rest/getBindings.do"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    data ={
        "userName": settings.JCC_API_USERNAME,
        "password": settings.JCC_API_PASSWORD,
        "clientId": client_id,
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()
        
        if response_data.get("errorCode") == "0":
            binding_id = response_data.get("bindings", [])
            return binding_id
        else:
            error_message = response_data.get("errorMessage")
            return error_message

    except Exception as e:
        return str(e)


    
    