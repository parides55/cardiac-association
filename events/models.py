from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

STATUS = ((0, "Draft"), (1, "Published"))

class Event(models.Model):
    
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = CloudinaryField('image', default='placeholder')
    content = models.TextField()
    date_of_event = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    excerpt = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    def __str__(self):
        return f"{self.title} - {self.created_on.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['-created_on']