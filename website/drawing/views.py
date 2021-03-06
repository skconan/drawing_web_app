from django.shortcuts import render, redirect
from .forms import UploadForm
from django.http import HttpResponse
from image_processing.image_processing import *
from image_processing.models import Image
import random
import website.settings as settings
from django.db.models import Q

from image_processing.models import Image as ImageTable
from .models import VideoUpload as VideoTable
from .models import Mission as MissionTable
import os

PATH_IMG = settings.MEDIA_URL+"dataset/images/"



# Create your views here.
def label(req):
    global mission_name
    images_list = ImageTable.objects.all()
    number_of_img = images_list.count()
    number_of_label = ImageTable.objects.filter(is_label=True).count()
    context = {}
    template = 'label.html'

    mission_list = MissionTable.objects.all()
    mission_name = []
    mission_name_no = []
    for m in mission_list:
        mission_name.append(m.name)
        mission_name_no.append([m.name,m.labeled])

    
    if req.method == 'POST':
        print("POST")
        

        
        image_name = req.POST['image-name']
        
        if 'delete' in req.POST:
            Image.objects.filter(name=image_name).delete()
            if os.path.exists(settings.MEDIA_ROOT+"/dataset/images/" + image_name + '.jpg'):
                os.remove(settings.MEDIA_ROOT+"/dataset/images/" + image_name + '.jpg')
                print("removed")
        else:
            for m in mission_name:
                try:
                    print(m+">"+req.POST['checkbox-'+m])
                    mtable = MissionTable.objects.filter(name=m)[0]
                    if req.POST['checkbox-'+m] == 'check':
                        print(m, 'update labeled')
                        print("a",mtable.labeled)
                        no = mtable.labeled + 1
                        print("b",mtable.labeled,no)
                        MissionTable.objects.filter(name=m).update(labeled = no)
                except:
                    pass

            image_data = req.POST['mask-result']

            save_canvas(image_data,image_name)
            i = Image.objects.get(name=image_name)
            i.is_label = True
            i.save()
        return redirect('label')
    else:      
        mission_list = MissionTable.objects.all()
        mission_name = []
        min = 100000000
        min_name = ""
        for m in mission_list:
            mission_name.append(m.name)
            if m.labeled < min:
                min_name = m.name
        if "mission" in req.session:
            min_name = req.session["mission"]
        print(min_name)
        i = Image.objects.filter(Q(is_label=False) & (
             Q(mission_1=min_name) |
             Q(mission_2=min_name) |
             Q(mission_3=min_name) |
             Q(mission_4=min_name) |
             Q(mission_5=min_name)) ).all()
        
        print(len(i))
        index = random.randint(0,len(i)-1)
        image_name = i[index].name
    
        image_url = settings.MEDIA_URL + 'dataset/images/'+image_name+".jpg"
 
        context = {
            'img_name':image_name,
            'img_url':image_url,
            'no_img' : number_of_img,
        'no_label' : number_of_label,
        'mission_name_no' :mission_name_no,
        }
    return render(req, template, context)

def upload(req):
    template = 'upload.html'
    mission_n = range(1,6)

    mission_list = MissionTable.objects.all()
    mission_name = []
    for m in mission_list:
        mission_name.append(m.name)

    if req.method == 'POST':
        mission_list = []
        for i in mission_n:
            # print(i)
            txt_box = "textbox_mission_"+str(i)
            if txt_box in req.POST:
                # print(req.POST[txt_box])
                mission_list.append(req.POST[txt_box])
            # print("----")
        form = UploadForm(req.POST, req.FILES)
        if form.is_valid():
            # form.save()
            form = form.save(commit=False)
            form.original_filename = req.FILES['video'].name
            form.name = req.FILES['video'].name
            form.save()
            video2img(req.FILES['video'].name,15, mission_list)
            return render(req, "status.html", {"status":"Video Uploaded"})
    else:
        form = UploadForm()
    context = {'form':form, 'mission_n':mission_n, 'mission_name':mission_name}
    return render(req, template, context)

def select_mission(req):
    template = 'select_mission.html'


    mission_list = MissionTable.objects.all()
    mission_name = []
    for m in mission_list:
        mission_name.append(m.name)

    if req.method == 'POST':
        txt_box = "textbox_mission"
        if len(req.POST[txt_box]) > 0:
            req.session['mission'] = req.POST[txt_box]
            return HttpResponse("mission "+req.POST[txt_box]+" is selected")


    context = {'mission_name':mission_name}
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


def reset_is_label(req):
    images_list = ImageTable.objects.all()
    images_list.update(is_label=False)
    return HttpResponse("Done")

def dataset(req,page=1):
    images_list = ImageTable.objects.all()
    number_of_img = images_list.count()
    number_of_label = ImageTable.objects.filter(is_label=True).count()
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
