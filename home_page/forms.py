from django import forms
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
        self.fields['heart_disease'].label = "Heart Disease"
        self.fields['date_of_diagnosis'].label = "Date of Diagnosis"
        self.fields['registered_as'].label = "Registered_as"
