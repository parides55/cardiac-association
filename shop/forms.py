from django import forms
from .models import Basket


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