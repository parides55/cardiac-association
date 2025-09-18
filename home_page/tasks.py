import requests
import uuid
import logging
from background_task import background
from django.contrib.staticfiles import finders
from django.core.mail import EmailMultiAlternatives, mail_admins
from dateutil.relativedelta import relativedelta
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
    
    try:
        renewed_members_list = []
        if not members_for_renewal.exists():
            subject = "Members for renewal"
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
                payment_response = make_payment(unique_order_number, member_client_id, binding_id, member.id)

                # Send email notification to the member
                send_email_for_renewal(member)
                renewed_members_list.append((member.name, member.surname, member.id_number))

            if renewed_members_list:
                subject = "Members renewed successfully"
                text_content = f"The following members have been renewed:\n" + "\n".join([f"{name} {surname} ({id_number})" for name, surname, id_number in renewed_members_list])
                mail_admins(subject, text_content)

    except Exception as e:
        subject = "Error in renewal task"
        text_content = f"An error occurred: {str(e)}"
        mail_admins(subject, text_content)


def get_credentials(client_id):

    url = "https://gateway.jcc.com.cy/payment/rest/getBindings.do"
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


def make_payment(order_number, client_id, binding_id, member_id):
    
    url = "https://gateway.jcc.com.cy/payment/rest/instantPayment.do"
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
            # Update the member's next payment date
            member = Member.objects.get(id=member_id)
            member.next_payment_date = timezone.now() + relativedelta(years=1)
            member.save()
            return payment_response
        else:
            # Update the member's status to expired
            member = Member.objects.get(id=member_id)
            member.membership_status = "expired"
            member.save()
            error_message = response_data.get("errorMessage")
            return error_message
    except Exception as e:
        return str(e)


def send_email_for_renewal(member):
    
    logger = logging.getLogger(__name__)
    
    subject = "Σας ευχαριστούμε που είστε πάντα δίπλα μας!"
    
    from_email = settings.EMAIL_HOST_USER
    to_email = [member.email]
    
    html_content = f"""
    <html>
        <body>
            <p>Αγαπητέ/ή {member.name} {member.surname}<br><br></p>
            <p>
                Θα θέλαμε να σας ευχαριστήσουμε από καρδιάς για την ανανέωση της ετήσιας 
                συνδρομής σας στον <strong>Σύνδεσμο Γονέων και Φίλων Καρδιοπαθών Παιδιών.</strong><br><br> 
                Η σταθερή σας υποστήριξη είναι πραγματικά πολύτιμη για εμάς. Χάρη σε μέλη όπως εσείς, 
                μπορούμε να συνεχίζουμε να στεκόμαστε δίπλα στα παιδιά με καρδιοπάθειες και 
                στις οικογένειές τους, προσφέροντας βοήθεια, στήριξη και ελπίδα.<br><br>Αν έχετε 
                χρόνο και διάθεση, θα χαρούμε πολύ να σας δούμε και πιο ενεργά κοντά μας – 
                είτε μέσα από τις δράσεις μας, είτε συμμετέχοντας εθελοντικά σε εκδηλώσεις ή 
                απλώς διαδίδοντας το έργο μας.<br>Μαζί μπορούμε να κάνουμε ακόμα περισσότερα!<br><br><br>
            </p>
            <p>
                Με εκτίμηση,<br><br>
                
                <strong>Σύνδεσμος Γονέων και Φίλων Παιδιών με Καρδιοπάθειες</strong><br>
                <img src="cid:default_logo.jpg" alt="Association's Logo" width="100px" height=auto><br>
                <a href="pediheart.org.cy">pediheart.org.cy</a><br>
                Οδός Γράμμου 11, Διαμέρισμα 5,
                Στρόβολος, Λευκωσία, Κύπρος<br><br>
                Tel: <a href="tel:+35722315196">22315196</a><br>
                Mail: <a href="mailto:info@pediheart.org.cy">info@pediheart.org.cy</a><br><br>
            </p>
            <p>
                <strong>Σημείωση:</strong> Εάν θέλετε να τερματίσετε την συνδρομή σας,
                μπορείτε να το κάνετε <a href="https://pediheart.org.cy/en/cancel_membership/">πατώντας εδώ</a>.
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
        
check_member_for_renewal()