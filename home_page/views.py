import os
import requests
import uuid
import logging
from logging import Logger
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.staticfiles import finders
from django.core.mail import EmailMultiAlternatives, mail_admins
from django.conf import settings
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
def become_member(request):

    try:
        if request.method == 'POST':
            member_form = MemberForm(request.POST)
            if member_form.is_valid():
                new_member = member_form.save(commit=False)
                new_member.save()
                # messages.success(request, f"Welcome to the family of the Association of Children with Heart Disease." 
                #     f"Your membership has been successfully registered.")
                # return render(request, "home_page/index.html")
                
                # Process payment
                # Append a random 8-character string to the orderId to make it unique
                unique_order_number = f"{new_member.id}-{uuid.uuid4().hex[:8]}"
                try:
                    payment_url = process_payment(unique_order_number)
                    return redirect(payment_url) # Redirect user to JCC payment page
                except Exception as e:
                    messages.error(request, f"An error occurred while processing your payment: {str(e)}")
                    return redirect('home')
            else:
                messages.error(
                    request,
                    f"The following error occurred while processing your request:'{member_form.errors}'\n" 
                    f"Please try completing the form again or contact us."
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

    url = "https://gateway-test.jcc.com.cy/payment/rest/register.do"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {
        "amount": 2000,
        "currency": "978",  # EUR currency code
        "userName": settings.JCC_API_USERNAME,
        "password": settings.JCC_API_PASSWORD,
        "returnUrl": f"https://pediheart.org.cy/membership_success/{orderId}",
        "failUrl": f"https://pediheart.org.cy/membership_failed/{orderId}",
        "description": "Membership fee of the Association of Children with Heart Disease",
        "language": "en",
        "orderNumber": orderId,
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

            orderId = orderId.split("-")[0] # Get the original orderId

            # Mark member as paid in the database
            member = Member.objects.get(id=orderId)
            member.last_payment_date = timezone.now()
            member.is_paid = True
            member.save()

            # After successful payment, send a welcome email to the member
            send_welcome_email(member)
            send_email_to_the_admin(member)

            messages.success(request, f"Welcome to the family of the Association of Children with Heart Disease." 
                            f"Your membership has been successfully registered.")
            return render(request, "home_page/index.html")
        else:
            messages.error(request, "Payment verification failed. Try again or contact us for further assistance.")
            return render(request, "home_page/index.html",)
    except Exception as e:
        messages.error(request, f"An error occurred while verifying your payment: {str(e)}")
        return render(request, "home_page/index.html",)


def membership_failed(request, orderId):
    
    """Handle failed payment and delete the member from the database."""
    
    orderId = orderId.split("-")[0]  # Get the original orderId
    member = get_object_or_404(Member, id=orderId)
    member.delete()
    
    messages.error(request, "Payment failed. Please try again or contact us for further assistance.")
    return render(request, "home_page/index.html",)


def send_welcome_email(member):
    
    logger = logging.getLogger(__name__)
    
    subject = "Καλωσορίσατε στην οικογένεια του Σύνδεσμου Γονέων και Φίλων Παιδιών με Καρδιοπάθειες"
    from_email = settings.EMAIL_HOST_USER
    to_email = [member.email]
    
    html_content = f"""
        <html>
            <body>
                <p>Αγαπητέ/ή {member.name} {member.surname}<br><br></p>
                <p>
                    Με μεγάλη χαρά σας καλωσορίζουμε ως μέλος του Συνδέσμου Γονέων και Φίλων Καρδιοπαθών παιδιών! 
                    Η υποστήριξή σας στα παιδιά με καρδιοπάθειες είναι ανεκτίμητη, και εκτιμούμε 
                    βαθύτατα τη γενναιοδωρία σας.<br><br>
                    Με τη συνδρομή σας των 20€ ετησίως, συμβάλλετε άμεσα σε προγράμματα που παρέχουν 
                    απαραίτητη ιατρική φροντίδα, συναισθηματική στήριξη και πόρους για τις οικογένειες 
                    που το έχουν ανάγκη. Η συνεισφορά σας μας βοηθά να συνεχίσουμε το έργο μας και να 
                    κάνουμε τη διαφορά στη ζωή αυτών των παιδιών.<br><br>
                    Ως μέλος μας, θα λαμβάνετε ενημερώσεις για τις δράσεις μας, τις εκδηλώσεις και τους 
                    τρόπους με τους οποίους μπορείτε να συμμετάσχετε πιο ενεργά. Είμαστε ενθουσιασμένοι 
                    που σας έχουμε μαζί μας σε αυτή την όμορφη προσπάθεια.<br><br>
                    Εάν έχετε οποιαδήποτε ερώτηση ή θέλετε να μάθετε περισσότερα για τον αντίκτυπο της 
                    προσφοράς σας, μη διστάσετε να επικοινωνήσετε μαζί μας.<br>
                    Σας ευχαριστούμε από καρδιάς για την καλοσύνη και τη γενναιοδωρία σας. Μαζί, 
                    μπορούμε να δώσουμε ελπίδα στις μικρές καρδιές!<br><br><br>
                </p>
                <p>
                    Με εκτίμηση,<br><br>
                    
                    <strong>Σύνδεσμος Γονέων και Φίλων Παιδιών με Καρδιοπάθειες</strong><br>
                    <img src="cid:default_logo.jpg" alt="Association's Logo" width="100px" height=auto><br>
                    <a href="pediheart.org.cy">pediheart.org.cy</a><br>
                    Οδός Γράμμου 11, Διαμέρισμα 5,
                    Στρόβολος, Λευκωσία, Κύπρος<br><br>
                    Tel: <a href="tel:+35722315196">22315196</a><br>
                    Mail: <a href="mailto:pediheart@cytanet.com.cy">pediheart@cytanet.com.cy</a><br><br>
                </p>
            </body>
        </html>
        """
        
    email = EmailMultiAlternatives(subject, "", from_email, to_email)
    email.attach_alternative(html_content, "text/html")

    # Locate the image in the static folder
    logo_path = finders.find("images/default_logo.jpg")

    if logo_path:
        try:
            with open(logo_path, "rb") as logo_file:
                email.attach("default_logo.jpg", logo_file.read(), "image/jpeg")
        except Exception as e:
            logger.error(f"Failed to attach logo image: {e}")
    else:
        logger.warning("Logo image not found: static/images/default_logo.jpg")

    try:
        email.send()
        logger.info(f"Welcome email successfully sent to {member.email}")
    except Exception as e:
        logger.error(f"Failed to send welcome email to {member.email}: {e}")


def send_email_to_the_admin(member):
    
    subject = "Νέο μέλος στον Σύνδεσμο Γονέων και Φίλων Παιδιών με Καρδιοπάθειες"
    
    html_content = f"""
        <html>
            <body>
                <p>Νέο μέλος:</p>
                <p>Όνομα: {member.name}</p>
                <p>Επώνυμο: {member.surname}</p>
                <p>Email: {member.email}</p>
                <p>Τηλέφωνο: {member.phone_number}</p>
                <p>Ημερομηνία Εγγραφής: {member.date_joined}</p>
                <p>Πληρωμένο: {member.is_paid}</p>
                <br><br>
                <p>Παρακαλώ ελέγξτε τις λεπτομέρειες του νέου μέλους στη βάση δεδομένων.</p>
            </body>
        </html>
    """
    
    mail_admins(subject, "", html_message=html_content)