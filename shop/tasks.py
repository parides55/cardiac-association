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
def check_subscriptions_for_payment():
    """
    Check subscriptions for payment and process them.
    """
    today = timezone.localdate()

    donors_for_payment = Donation.objects.annotate(
        next_payment_date_only=TruncDate('next_payment_date')).filter(
        status="active", donation_type="Monthly Subscription",
        next_payment_date_only=today
    )
    
    try:
        donors_for_payment_list = []
        if not donors_for_payment.exists():
            subject = "Donors for payment"
            text_content = "There are no donors for payment today."
            mail_admins(subject, text_content)
        else:
            for donor in donors_for_payment:
                donor_client_id = donor.client_id

                store_credentials = get_credentials(donor_client_id)

                if isinstance(store_credentials, list) and store_credentials:
                    # Get the first bindingId
                    binding_id = store_credentials[0].get("bindingId", "No binding ID found")
                else:
                    binding_id = f"Error or no bindings: {store_credentials}"
                
                # Make the payment
                unique_order_number = f"{donor.id}-{uuid.uuid4().hex[:8]}"
                amount = int(float(donor.donation_amount) * 100)  # Convert to cents
                payment_response = make_payment(unique_order_number, donor_client_id, binding_id, donor.id, amount)

                # Send email notification to the member
                send_email_for_renewal(donor)
                donors_for_payment_list.append((donor.full_name, donor.id))

            if donors_for_payment_list:
                subject = "Donors for payment"
                text_content = f"The following donors have paid the monthly subscription today:\n" + "\n".join([f"{name} ({id})" for name, id in donors_for_payment_list])
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


def make_payment(order_number, client_id, binding_id, donor_id,amount):
    
    url = "https://gateway.jcc.com.cy/payment/rest/instantPayment.do"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    data = {
        "userName": settings.JCC_API_USERNAME,
        "password": settings.JCC_API_PASSWORD,
        "orderNumber": order_number,
        "amount": amount,  # Amount in cents
        "currency": 978,  # Euro
        "clientId": client_id,
        "bindingId": binding_id,
        "tii": "U",
        "backUrl": "https://example.com/success",
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()
        donor = Donation.objects.get(id=donor_id)
        
        if response_data.get("errorCode") == "0":
            payment_response = response_data.get("orderStatus")
            # Update the donor's next payment date
            donor.next_payment_date = timezone.now() + relativedelta(months=1)
            donor.save()
            return payment_response
        else:
            # Update the donor's status to expired
            donor.status = "expired"
            donor.save()
            error_message = response_data.get("errorMessage")
            return error_message
    except Exception as e:
        return str(e)


def send_email_for_renewal(donor):
    
    logger = logging.getLogger(__name__)
    
    subject = "Σας ευχαριστούμε που είστε πάντα δίπλα μας!"
    
    from_email = settings.EMAIL_HOST_USER
    to_email = [donor.email]
    
    html_content = f"""
    <html>
        <body>
            <p>Αγαπητέ/ή {donor.full_name}<br><br></p>
            <p>
                Εκ μέρους όλων μας στον <strong>Σύνδεσμο Γονέων και Φίλων Καρδιοπαθών Παιδιών.</strong>, 
                θα θέλαμε να σας εκφράσουμε την ειλικρινή μας ευγνωμοσύνη για τη συνεχή μηνιαία σας δωρεά, 
                με το πσοό των €{donor.donation_amount}.<br><br>
                Η γενναιοδωρία σας κάνει πραγματική διαφορά στη ζωή των παιδιών με καρδιοπάθειες και των 
                οικογενειών τους. Χάρη στη δική σας στήριξη, μπορούμε να προσφέρουμε ουσιαστικές 
                υπηρεσίες, ψυχολογική υποστήριξη και προγράμματα που φέρνουν ελπίδα και ανακούφιση σε όσους 
                το έχουν ανάγκη.<br><br>Η σταθερή σας δέσμευση σημαίνει πολλά για εμάς — και ακόμα περισσότερα 
                για τα παιδιά που βοηθάτε κάθε μήνα.<br><br>
                Παρακάτω θα βρείτε τα στοιχεία της δωρεάς σας:<br><br>
                Μοναδικός αρ. δωρεάς: {donor.id}<br>
                Ποσό Δωρεάς: €{donor.donation_amount}<br>
                Τύπος Δωρεάς: {donor.donation_type}<br><br>
                Σας ευχαριστούμε που είστε δίπλα μας. Μαζί, 
                δημιουργούμε ένα καλύτερο και πιο υγιές μέλλον για τα παιδιά με καρδιοπάθειες.
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
                <strong>Σημείωση:</strong> Εάν θέλετε να τερματίσετε την εγγραφή σας,
                μπορείτε να το κάνετε <a href="https://pediheart.org.cy/en/shop/cancel_monthly_donation/">πατώντας εδώ</a>.
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
        logger.info(f"Welcome email successfully sent to {donor.email}")
    except Exception as e:
        logger.error(f"Failed to send welcome email to {donor.email}: {e}")

