import requests
from background_task import background
from django.core.mail import mail_admins
from datetime import datetime
from django.conf import settings
from .models import *


@background(schedule=60)
def check_member_for_renewal():
    
    today = datetime.today().date()
    
    members_for_renewal = Member.objects.filter(membership_expiry_date__lte=today,)
    
    subject = "Membership Expiry Reminder"
    
    text_content = f""""
    Tme members for renewal are :
    
    {members_for_renewal}
    """           

    mail_admins(subject, text_content)

# def get_credentials(client_id):

#     url = "https://gateway-test.jcc.com.cy/payment/rest/getBindings.do"
#     headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
#     data ={
#         "userName": settings.JCC_USERNAME,
#         "password": settings.JCC_PASSWORD,
#         "clientId": client_id,
#     }
    
#     try:
#         response = requests.post(url, headers=headers, data=data)
#         response_data = response.json()
        
#         if response_data.get("errorCode") == "0":
#             binding_id = response_data.get("bindings", [])
#             return binding_id
#         else:
#             error_message = response_data.get("errorMessage")
#             return error_message

#     except Exception as e:
#         return str(e)


    
    