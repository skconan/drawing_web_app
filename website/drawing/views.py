from django.shortcuts import render
from .forms import UploadForm
from django.http import HttpResponse
from image_processing.image_processing import *
# Create your views here.
def masker(req):
    template = 'masker.html'
    context = {}

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