from .views import charge_recurring_payment
from .models import Member
from celery import shared_task

@shared_task
def process_recurring_payments():
    """Find active subscriptions and process their payments."""
    members = Member.objects.filter(is_active=True)  # Get all active subscriptions
    for member in members:
        charge_recurring_payment(member)  # Process the payment
