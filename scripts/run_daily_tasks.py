from home_page.tasks import check_member_for_renewal
from shop.tasks import check_subscriptions_for_payment


def run():
    check_member_for_renewal()
    check_subscriptions_for_payment()