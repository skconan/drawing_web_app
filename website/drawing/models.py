from django.db import models

# Create your models here.

class VideoUpload(models.Model):
    video = models.FileField(upload_to='')