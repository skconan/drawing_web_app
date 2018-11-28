from django.shortcuts import render
from .forms import UploadForm
from django.http import HttpResponse
from image_processing.image_processing import *
from image_processing.models import Image
import random

# Create your views here.
def masker(req):
    template = 'masker.html'
    img_name = '1543344041.jpg';
    img_url = 'http://127.0.0.1:8000/media/dataset/images/'+img_name
    i = Image.objects.filter(mask=False)
    index = random.randint(0,len(i)-1)
    image_name = i[index].name
    context = {'img_name':image_name}
    return render(req, template, context)

def upload(req):
    template = 'upload.html'
    if req.method == 'POST':
        print(req)

        form = UploadForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            form = form.save(commit=False)
            form.original_filename = req.FILES['video'].name
            form.save()
            video2img(req.FILES['video'].name,10)
            return HttpResponse('home')
    else:
        form = UploadForm()
    context = {'form':form}
    return render(req, template, context)