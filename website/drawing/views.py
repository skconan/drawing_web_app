from django.shortcuts import render, redirect
from .forms import UploadForm
from django.http import HttpResponse
from image_processing.image_processing import *
from image_processing.models import Image
import random
import website.settings as settings

from image_processing.models import Image as ImageTable
from .models import VideoUpload as VideoTable

PATH_IMG = settings.MEDIA_URL+"dataset/images/"

# Create your views here.
def label(req):
    images_list = ImageTable.objects.all()
    number_of_img = images_list.count()
    number_of_label = ImageTable.objects.filter(mask=True).count()
    context = {}
    template = 'label.html'
    if req.method == 'POST':
        print("POST")
        image_data = req.POST['mask-result']
        image_name = req.POST['image-name']
        save_canvas(image_data,image_name)
        i = Image.objects.get(name=image_name)
        i.mask = True
        i.save()
        return redirect('label')
    else:      
        i = Image.objects.filter(mask=False)
        index = random.randint(0,len(i)-1)
        image_name = i[index].name
    
        image_url = settings.MEDIA_URL + 'dataset/images/'+image_name+".jpg"
 
        context = {
            'img_name':image_name,
            'img_url':image_url,
            'no_img' : number_of_img,
        'no_label' : number_of_label,
        }
    return render(req, template, context)

def upload(req):
    template = 'upload.html'
    if req.method == 'POST':
        print(req)
        form = UploadForm(req.POST, req.FILES)
        if form.is_valid():
            # form.save()
            form = form.save(commit=False)
            form.original_filename = req.FILES['video'].name
            form.name = req.FILES['video'].name
            form.save()
            video2img(req.FILES['video'].name,15)
            return render(req, "status.html", {"status":"Video Uploaded"})
    else:
        form = UploadForm()
    context = {'form':form}
    return render(req, template, context)

def index(req):
    template = 'index.html'
    # if req.method == 'POST':
    #     print(req)
    #     form = UploadForm(req.POST, req.FILES)
    #     if form.is_valid():
    #         # form.save()
    #         form = form.save(commit=False)
    #         form.original_filename = req.FILES['video'].name
    #         form.name = req.FILES['video'].name
    #         form.save()
    #         video2img(req.FILES['video'].name,15)
    #         return HttpResponse('home')
    # else:
    #     form = UploadForm()
    # context = {'form':form}
    context = {}
    return render(req, template, context)


def dataset(req,page=1):
    images_list = ImageTable.objects.all()
    number_of_img = images_list.count()
    number_of_label = ImageTable.objects.filter(mask=True).count()
    # images_list = images_list.order_by('-created_date')

    data = []
    count = 0
    data_per_page = 30
    
    start_index = (page-1)*data_per_page
    stop_index = page*data_per_page
    d = []
    for img in images_list[start_index:stop_index]:
        image_url = settings.MEDIA_URL + 'dataset/images/'+img.name+".jpg"
        count += 1
        d.append([image_url, str(img.name)])
        if count == 5:
            data.append(d)
            d = []
            count = 0

    # page_list = list(range(1,len(images_list)//data_per_page + 1))[:10]
    page_list = list(range(page,page + 11))
    print(page_list)
    
    field = {
        'no_img' : number_of_img,
        'no_label' : number_of_label,
        'data':data,
        'page':page_list,
        'current_page':page, 
        'next_page' : page + 1, 
        'previous_page' : page - 1
    }
    # for f in csv_file:
    #     file_list["name"].append(name)
    # file_list["url"].append(f)
        #  "url": f}
    context = {'field':field}
    template = 'dataset.html'
    return render(req, template, context)

def videos(req,page=1):
    vdo_list = VideoTable.objects.all()
    number_of_vdo = vdo_list.count()
    # number_of_label = ImageTable.objects.filter(mask=True).count()
    # vdo_list = vdo_list.order_by('-created_date')

    data = [[]]*2
    count = 0
    data_per_page = 40
    
    start_index = (page-1)*data_per_page
    stop_index = page*data_per_page
    stop = min(stop_index,len(vdo_list))
    print(stop)
    for vdo in vdo_list[start_index:stop]:
        image_url = settings.MEDIA_URL + 'videos/'+vdo.name
        data[count].append([image_url, str(vdo.name)])
        count += 1
        if count == 2:
            count = 0

    # page_list = list(range(1,len(vdo_list)//data_per_page + 1))[:10]
    page_list = list(range(page,page + 2))
    print(page_list)
    
    field = {
        'no_vdo' : number_of_vdo,
        # 'no_label' : number_of_label,
        'data':data,
        'page':page_list,
        'current_page':page, 
        'next_page' : page + 1, 
        'previous_page' : page - 1
    }
    # for f in csv_file:
    #     file_list["name"].append(name)
    # file_list["url"].append(f)
        #  "url": f}
    context = {'field':field}
    template = 'videos.html'
    return render(req, template, context)
