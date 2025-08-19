from django.core.management.base import BaseCommand
from .tasks import check_member_for_renewal
from shop.tasks import check_subscriptions_for_payment

class Command(BaseCommand):
    help = 'Run daily tasks'

    def handle(self, *args, **options):
        check_member_for_renewal()
        check_subscriptions_for_payment()