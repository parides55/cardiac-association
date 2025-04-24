from background_task import background
from django.core.mail import mail_admins
from datetime import datetime
from django.conf import settings

@background(schedule=60)  # Runs 60 seconds after being scheduled
def my_scheduled_task():
    subject = f"Task executed at {datetime.now()}"

    text_content = f"""
    This is a scheduled task that runs every 60 seconds.
    """

    mail_admins(subject, text_content)
