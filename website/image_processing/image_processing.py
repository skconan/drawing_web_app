import cv2 as cv
import time
from .models import Image
from website import settings

PATH_IMG = settings.MEDIA_ROOT+"dataset/images/"


def record(image_name):
    i = Image(image_name, False)
    i.save()


def video2img(file_name, sampling):
    file_path = settings.MEDIA_ROOT+"videos/"+file_name
    cap = cv.VideoCapture(file_path)
    count = 0
    count_false = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            count_false += 1
            if count_false > 30:
                cap.release()
                break
            continue
        
        if count % sampling == 0 and ret:
            image_name = str(time.time())[:10]
            c = 484  # //1936 / 4
            r = 304  # //1216 / 4
            img = cv.resize(frame,(c,r))
            cv.imwrite(PATH_IMG + "\\" + image_name + ".jpg", img)
            record(image_name)
            count_false = 0

        count += 1
