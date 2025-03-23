from celery import shared_task

@shared_task
def charge_annual_subscription():
    return 'Annual subscription charged'