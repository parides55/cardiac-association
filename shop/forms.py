from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Basket, Donation, ShippingDetail


class BasketForm(forms.ModelForm):
    """
    A form for users to add items to their basket.
    """
    class Meta:
        """
        Specify the django model and fields to be displayed.
        """
        model = Basket
        fields = ['quantity', ]
    
    def __int__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].label=_('Quantity')


class ShippingDetailForm(forms.ModelForm):
    """
    A form for users to enter their shipping details.
    """
    class Meta:
        """
        Specify the django model and fields to be displayed.
        """
        model = ShippingDetail
        fields = [
            'full_name',
            'email',
            'phone_number',
            'address_for_delivery',
            'city',
            'area',
            'postcode',
            ]
    
    def __int__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].label=_('Full Name')
        self.fields['email'].label=_('Email')
        self.fields['phone_number'].label=_('Phone Number')
        self.fields['address_for_delivery'].label=_('Address for Delivery')
        self.fields['city'].label=_('City')
        self.fields['area'].label=_('Area')
        self.fields['postcode'].label=_('Postcode')


class DonationForm(forms.ModelForm):
    """
    A form for users to make a donation.
    """
    class Meta:
        """
        Specify the django model and fields to be displayed.
        """
        model = Donation
        fields = [
            'full_name',
            'email',
            'phone_number',
            'address',
            'city',
            'area',
            'postcode',
            'donation_amount',
            'donation_type',
            ]
    
    def __int__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].label=_('Full Name')
        self.fields['email'].label=_('Email')
        self.fields['phone_number'].label=_('Phone Number')
        self.fields['address'].label=_('Address')
        self.fields['city'].label=_('City')
        self.fields['area'].label=_('Area')
        self.fields['postcode'].label=_('Postcode')
        self.fields['donation_amount'].label=_('Donamtion Ammount')
        self.fields['donation_type'].label=_('Doantion Type')
