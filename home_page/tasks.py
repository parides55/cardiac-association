import requests
from background_task import background
from django.core.mail import mail_admins
from datetime import datetime
from django.conf import settings
from .models import *

@background(schedule=60)
def check_member_for_renewal():
    
    for member in Member.object.all():
        if member.membership_status == 'active' and member.next_payment_date == datetime.today():
            member_client_id = member.client_id
            
        try:
            stored_credentials = get_credentials(member_client_id)
            
            subject = "Membership Renewal"
            
            text_content = f"""
            The membership for {member.name} {member.surname} is due for renewal.
            
            The stored credentials/error messages are: {stored_credentials}
            """
            
            mail_admins(subject, text_content)
        
        except Exception as e:
            error_message = f"Error checking member {member.name} {member.surname}: {str(e)}"
            mail_admins("Error in Membership Renewal Check", error_message)
                
    

    

    
def get_credentials(client_id):

    url = "https://gateway-test.jcc.com.cy/payment/rest/getBindings.do"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    data ={
        "userName": settings.JCC_USERNAME,
        "password": settings.JCC_PASSWORD,
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


    
    