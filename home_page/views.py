from django.shortcuts import render, get_object_or_404, reverse, redirect
import requests
from django.conf import settings
from django.contrib import messages
from .forms import MemberForm
from .models import Member


# Home page view
def index(request):
    return render(request, "home_page/index.html")


# More Information page about heart disease view
def MoreInfo(request):
    return render(request, "home_page/heart_disease_info.html")


# Become a member views
def process_payment(orderId):
    url = "https://gateway-test.jcc.com.cy/payment/rest/register.do"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}  

    data = {
        "amount": 2000,
        "currency": "978",  # EUR currency code
        "userName": settings.JCC_API_USERNAME,
        "password": settings.JCC_API_PASSWORD,
        "returnUrl": f"https://pediheart.org.cy/membership_success/{orderId}",
        "failUrl": f"https://pediheart.org.cy/membership_failed/",
        "description": "Membership fee of the Association of Children with Heart Disease",
        "language": "en",
        "orderNumber": orderId
    }

    try:
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            response_data = response.json()
            if "formUrl" in response_data:
                return response_data["formUrl"]  # Redirect user to JCC payment page
            else:
                raise Exception(f"JCC Error: {response_data.get('errorMessage', 'Unknown error')}")
        else:
            raise Exception(f"JCC API Request Failed: {response.status_code}, {response.text}")

    except Exception as e:
        raise Exception(f"The response from the JCC API failed: {e}")


def membership_success(request, orderId):

    memberId = request.GET.get("orderNumber")

    # Mark member as paid in the database
    member = Member.objects.get(id=orderId)
    member.is_paid = True
    member.save()

    messages.success(request, f"Welcome to the family of the Association of Children with Heart Disease." 
                    f"Your membership has been successfully registered.")
    return render(request, "home_page/index.html")


def membership_failed(request):
    
    messages.error(request, "Payment failed. Please try again or contact us for further assistance.")
    return render(request, "home_page/index.html",)


def Become_member(request):

    try:
        if request.method == 'POST':
            member_form = MemberForm(request.POST)
            print(member_form.errors)
            if member_form.is_valid():
                member_form.save()
                messages.success(request, f"Welcome to the family of the Association of Children with Heart Disease." 
                    f"Your membership has been successfully registered.")
                return render(request, "home_page/index.html")
                
                # # Process payment
                # try:
                #     payment_url = process_payment(member_form.instance.id)
                #     return redirect(payment_url) # Redirect user to JCC payment page
                # except Exception as e:
                #     messages.error(request, f"An error occurred while processing your payment: {str(e)}")
                #     return redirect('home_page/index.html')
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