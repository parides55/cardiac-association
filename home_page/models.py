from django.db import models

REGISTRATION_CHOICES = [
        ('sufferer', 'Sufferer'),
        ('parent', 'Parent'),
        ('friend', 'Friend'),
    ]

# Create you models here
class Member(models.Model):
    registered_as = models.CharField(max_length=20, choices=REGISTRATION_CHOICES, default='sufferer')
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    id_number = models.CharField(max_length=20, unique=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    home_number = models.CharField(max_length=20, blank=True, null=True)
    mobile_number = models.CharField(max_length=20)
    work_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField()
    heart_disease_description = models.CharField(max_length=100)
    date_of_diagnosis = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_payment_date = models.DateTimeField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.surname}"
