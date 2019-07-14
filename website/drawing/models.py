from django.db import models
from website import settings

# Create your models here.

class VideoUpload(models.Model):
    name = models.CharField(primary_key=True,max_length=50)
    video = models.FileField(upload_to="videos")
    def __str__(self):
        return self.name

class Mission(models.Model):
    name = models.CharField(primary_key=True,max_length=50)
    color = models.CharField(max_length=10)
    labeled = models.IntegerField()