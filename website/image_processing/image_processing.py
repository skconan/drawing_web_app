import cv2 as cv
import time
from .models import Image as Img
from website import settings
from io import BytesIO
from PIL import Image
import re
import base64
import numpy as np

PATH_IMG = settings.MEDIA_ROOT+"/dataset/images/"
PATH_GROUNDTRUTH = settings.MEDIA_ROOT+"/dataset/groundTruth/"


def record(image_name, mission_list):
    mission = []
    for m in mission_list:
        mission.append(m)
    i = Img(image_name, False, 
            mission[0],
            mission[1],
            mission[2],
            mission[3],
            mission[4],
            # mission[5],
            # mission[6],
            # mission[7],
            )
    i.save()


def video2img(file_name, sampling, mission_list):
    file_path = settings.MEDIA_ROOT+"/videos/"+file_name
    # print("File path:",file_path)
    cap = cv.VideoCapture(file_path)
    # print("Video2Image",cap.isOpened())
    count = 0
    count_false = 0
    while(cap.isOpened()):
        # print("Count",count)
        image_name = str(time.time()).replace(".","_")
        ret, frame = cap.read()
        if not ret:
            count_false += 1
            if count_false > sampling:
                cap.release()
                break
            continue

        if count % sampling == 0 and ret:
            
            c = 484  # //1936 / 4
            r = 304  # //1216 / 4
            img = cv.resize(frame, (c, r))
            cv.imwrite(PATH_IMG + image_name+ ".jpg", img)
            record(image_name, mission_list)
            count_false = 0
        count += 1

def save_canvas(image_data,image_name):
    im = canvas2img(image_data)
    im.save(PATH_GROUNDTRUTH+image_name+".png", 'PNG')

def canvas2img(image_data):
    # print(image_data)
    image_data = re.sub("^data:image/png;base64,", "", image_data)
    image_data = base64.b64decode(image_data)
    image_data = BytesIO(image_data)
    im = Image.open(image_data)
    return im
