from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
POSITIONS = ((0, "Πρόεδρος"), (1, "Αντιπρόεδρος"), (2, "Γραμματέας"), (3, "Βοηθός Γραμματέας"),
            (4, "Ταμίας"), (5,"Βοηθός Ταμίας"), (6, "Μέλος"), (7, "Προσωπικό"))


class People(models.Model):

    name = models.CharField(max_length=100)
    image = CloudinaryField('image', default='placeholder')
    position = models.IntegerField(choices=POSITIONS, default=0)

    def __str__(self):
        return f"{self.name} - {self.get_position_display()}"