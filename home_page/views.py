import os
import requests
import uuid
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.conf import settings
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from .forms import MemberForm
from .models import Member


# Home page view
def index(request):
    return render(request, "home_page/index.html")


# More Information page about heart disease view
def MoreInfo(request):
    return render(request, "home_page/heart_disease_info.html")


# Become a member views
def Become_member(request):

    try:
        if request.method == 'POST':
            member_form = MemberForm(request.POST)
            if member_form.is_valid():
                member_form.save()
                # messages.success(request, f"Welcome to the family of the Association of Children with Heart Disease." 
                #     f"Your membership has been successfully registered.")
                # return render(request, "home_page/index.html")
                
                # Process payment
                # Append a random 8-character string to the orderId to make it unique
                unique_order_number = f"{member_form.instance.id}-{uuid.uuid4().hex[:8]}"
                try:
                    payment_url = process_payment(unique_order_number)
                    return redirect(payment_url) # Redirect user to JCC payment page
                except Exception as e:
                    messages.error(request, f"An error occurred while processing your payment: {str(e)}")
                    return redirect('home')
            else:
                messages.error(
                    request,
                    f"There has been error processing your request. Please try completing "
                    f"the form again."
                )
                return render(request, "home_page/index.html")

        member_form = MemberForm()

        return render(
            request, "home_page/become_member.html",
            {'member_form': member_form}
        )

    except Exception as e:
        messages.error(request, f"The following error occurred: {str(e)}")
        return redirect('become_member')


def process_payment(orderId):

    url = "https://gateway-test.jcc.com.cy/payment/rest/instantPayment.do"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {
        "userName": settings.JCC_API_USERNAME,
        "password": settings.JCC_API_PASSWORD,
        "amount": 2000,
        "currency": "978",  # EUR currency code
        "orderNumber": orderId,
        "description": "Membership fee of the Association of Children with Heart Disease",
        "language": "en",
        "backUrl": f"https://pediheart.org.cy/membership_success/{orderId}",
        "failUrl": f"https://pediheart.org.cy/membership_failed/",
    }

    try:
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            response_data = response.json()
            if "redirect" in response_data:
                return response_data["redirect"]  # Redirect user to JCC payment page
            else:
                raise Exception(f"JCC Error: {response_data.get('errorMessage', 'Unknown error')}")
        else:
            raise Exception(f"JCC API Request Failed: {response.status_code}, {response.text}")

    except Exception as e:
        raise Exception(f"The response from the JCC API failed: {e}")


def membership_success(request, orderId):

    """Verify JCC payment success and store token for future charges."""
    
    verification_url = "https://gateway-test.jcc.com.cy/payment/rest/getOrderStatusExtended.do"
    headers = {"Content-type": "application/x-www-form-urlencoded"} 
    
    data = {
        "userName": settings.JCC_API_USERNAME,
        "password": settings.JCC_API_PASSWORD,
        "orderNumber": orderId,
    }
    
    try:
        response = requests.post(verification_url, headers=headers, data=data)
        response_data = response.json()

        if response_data.get("orderStatus") == 2:  # 2 means payment completed
            token = response_data.get("bindingId")  # Token for future payments
            messages.info(request, f"Token: {token}")

            orderId = orderId.split("-")[0] # Get the original orderId
            # Mark member as paid in the database
            member = Member.objects.get(id=orderId)
            member.recurring_token = token
            member.is_paid = True
            member.save()

            messages.success(request, f"Welcome to the family of the Association of Children with Heart Disease." 
                            f"Your membership has been successfully registered.")
            return render(request, "home_page/index.html")
        else:
            messages.error(request, "Payment verification failed. Try again or contact us for further assistance.")
            return render(request, "home_page/index.html",)
    except Exception as e:
        messages.error(request, f"An error occurred while processing your payment: {str(e)}")
        return render(request, "home_page/index.html",)


def membership_failed(request):
    
    messages.error(request, "Payment failed. Please try again or contact us for further assistance.")
    return render(request, "home_page/index.html",)


def charge_recurring_payment(member):
    """Charge the user for yearly subscriptions using their stored card token."""
    
    url = "https://gateway.jcc.com.cy/payment/rest/paymentOrderBinding.do"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    data = {
        "userName": os.getenv("JCC_API_USERNAME"),
        "password": os.getenv("JCC_API_PASSWORD"),
        "bindingId": member.recurring_token,  # The stored token
        "amount": 2000,
        "currency": "978",
        "orderNumber": f"RENEW-{member.id}-{datetime.now().strftime('%Y%m%d')}",
        "description": "Subscription Renewal",
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()

        if response_data.get("errorCode") == "0":  # Success
            member.last_payment_date = timezone.now()
            member.save()
            print(f"Recurring payment successful for Order ID: {member.id}")
        else:
            print(f"Recurring payment failed: {response_data.get('errorMessage')}")
    except Exception as e:
        print(f"An error occurred while processing recurring payment: {str(e)}")