from django.db import models

# Create your models here.
class Image(models.Model):
    name = models.CharField(primary_key=True,max_length=50)
    mask = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
