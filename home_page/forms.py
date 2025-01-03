from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'registered_as',
            'name', 
            'surname', 
            'email', 
            'id_number', 
            'profession', 
            'home_number', 
            'mobile_number', 
            'work_number', 
            'date_of_birth', 
            'heart_disease_description', 
            'date_of_diagnosis',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_diagnosis': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['registered_as'].label = _("Registered As")
        self.fields['name'].label = _("Name")
        self.fields['surname'].label = _("Surname")
        self.fields['email'].label = _("Email")
        self.fields['id_number'].label = _("ID Number")
        self.fields['profession'].label = _("Profession")
        self.fields['home_number'].label = _("Home Number")
        self.fields['mobile_number'].label = _("Mobile Number")
        self.fields['work_number'].label = _("Work Number")
        self.fields['date_of_birth'].label = _("Date of Birth")
        self.fields['heart_disease_description'].label = _(
            "Heart Disease Description (if not a sufferer, please write N/A)"
        )
        self.fields['date_of_diagnosis'].label = _("Date of Diagnosis")

