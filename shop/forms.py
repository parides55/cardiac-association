from django import forms
from .models import Basket, Donation


class BasketForm(forms.ModelForm):
    """
    A form for users to add items to their basket.
    """
    class Meta:
        """
        Specify the django model and fields to be displayed.
        """
        model = Basket
        fields = ('quantity', )


class DonationForm(forms.ModelForm):
    """
    A form for users to make a donation.
    """
    class Meta:
        """
        Specify the django model and fields to be displayed.
        """
        model = Donation
        fields = (
            'full_name', 'email', 'phone_number', 'address', 'address2',
            'city', 'state', 'postcode', 'donation_amount', 'donation_type',
            )