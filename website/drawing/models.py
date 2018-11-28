from django.db import models
from website import settings

# Create your models here.

class VideoUpload(models.Model):
    video = models.FileField(upload_to=settings.MEDIA_ROOT+"videos/")