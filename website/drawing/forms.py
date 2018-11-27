from django import forms
from .models import VideoUpload

class UploadForm(forms.ModelForm):
    class Meta:
        model = VideoUpload
        fields = ('video', )