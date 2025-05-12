import requests
import uuid
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
            
            if isinstance(store_credentials, list) and store_credentials:
                # Get the first bindingId
                binding_id = store_credentials[0].get("bindingId", "No binding ID found")
            else:
                binding_id = f"Error or no bindings: {store_credentials}"

            # Make the payment
            unique_order_number = f"{member.id}-{uuid.uuid4().hex[:8]}"
            payment_response = make_payment(unique_order_number, member_client_id, binding_id)

            subject = "Membership Expiry Reminder"

            text_content = f""""
            The payment response for {member.name} {member.surname} is as follows:

            {payment_response}

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


def make_payment(order_number, client_id, binding_id):
    
    url = "https://gateway-test.jcc.com.cy/payment/rest/instantPayment.do"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    data = {
        "userName": settings.JCC_API_USERNAME,
        "password": settings.JCC_API_PASSWORD,
        "orderNumber": order_number,
        "amount": 2000,  # Amount in cents
        "currency": 978,  # Euro
        "clientId": client_id,
        "bindingId": binding_id,
        "tii": "U",
        "backUrl": "https://example.com/success",
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()
        
        if response_data.get("errorCode") == "0":
            payment_response = response_data.get("orderStatus")
            return payment_response
        else:
            error_message = response_data.get("errorMessage")
            return error_message
    except Exception as e:
        return str(e)