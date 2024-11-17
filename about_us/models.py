from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
POSITIONS = ((0, "Chairman"), (1, "Vice Chairman"), (2, "Secretary"), (3, "Assistant Secretary"),
            (4, "Treasurer"), (5,"Assistant Treasurer"), (6, "Member"), (7, "Staff"))


class People(models.Model):
    name = models.CharField(max_length=100)
    image = CloudinaryField('image', default='placeholder')
    POSITIONS = models.IntegerField(choices=POSITIONS, default=0)