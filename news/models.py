from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

STATUS = ((0, "Draft"), (1, "Published"))


class New(models.Model):
    title_english = models.CharField(max_length=200, unique=True)
    title_greek = models.CharField(max_length=200, default='update in greek')
    slug = models.CharField(max_length=200, unique=True)
    image = CloudinaryField('image', default='placeholder')
    content_english = models.TextField()
    content_greek = models.TextField(default='update in greek')
    created_on = models.DateTimeField(auto_now_add=True)
    excerpt_english = models.TextField(blank=True)
    excerpt_greek = models.TextField(blank=True, default='update in greek')
    status = models.IntegerField(choices=STATUS, default=0)
    
    
    def __str__(self):
        return f"{self.title_greek} - {self.created_on.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['-created_on']