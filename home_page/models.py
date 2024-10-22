from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class HeroImage(models.Model):

    image = CloudinaryField('image', default='placeholder')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title, self.created_on
    
    class Meta:
        ordering = ['-created_on']