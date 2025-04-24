from background_task import background
from django.core.mail import mail_admins
from datetime import datetime
from django.conf import settings

@background(schedule=60)  # Runs 60 seconds after being scheduled
def my_scheduled_task_2():
    subject = f"Task executed at {datetime.now()}"

    text_content = f"""
    Hi!
    
    This is a scheduled task from the Shop running through the Heroku Scheduler.
    
    The time is now: {datetime.now()}
    
    It works too!
    """

    mail_admins(subject, text_content)
