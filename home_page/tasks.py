import requests
from background_task import background
from django.core.mail import mail_admins
from datetime import datetime
from django.conf import settings
from .models import *

@background(schedule=60)
def my_scheduled_task():
    url = "https://gateway-test.jcc.com.cy/payment/rest/getBindings.do"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    for member in Member.objects.all():
        if member.membership_status == 'active' and member.next_payment_date == datetime.today().date():
            member_client_id = member.client_id

            if not member_client_id:
                continue  # Skip if no client_id

            data = {
                "clientID": member_client_id,
                "userName": settings.JCC_API_USERNAME,
                "password": settings.JCC_API_PASSWORD,
            }

            try:
                response = requests.post(url, headers=headers, data=data)
                response.raise_for_status()  # Raise if HTTP error
                response_data = response.json()

                if response_data.get("errorCode") == 0:
                    stored_credentials = response_data.get("bindings", [])
                else:
                    raise Exception(f"JCC API Error: {response_data.get('errorCode')} - {response_data.get('errorMessage')}")

            except Exception as e:
                subject = "JCC API request failed"
                text_content = f"An error occurred while contacting JCC API for Member ID {member.id}:\n\n{str(e)}"
                mail_admins(subject, text_content)
                continue  # Move on to next member

            subject = f"Successful JCC API Request for Member ID {member.id}"
            text_content = f"""
            This is a test email to check the JCC API request for Member ID {member.id}.
            
            The request was made to the JCC API to get stored credentials.
            
            The response was: {response_data}
            
            The stored credentials are: {stored_credentials}
            """

            mail_admins(subject, text_content)
