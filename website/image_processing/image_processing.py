import cv2 as cv
import time
from .models import Image

PATH_IMG = r'C:\Users\skconan\Desktop\computer_vision\dataset\images'

def record(image_name):
    i = Image(image_name,False)
    i.save()

def video2img(file_path,sampling):
    file_path = r"C:\Users\skconan\Desktop\computer_vision\website\website\videos\\"+file_path
    cap = cv.VideoCapture(file_path)
    count = 0
    count_false = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        print(ret)
        if count % sampling == 0 and ret:
            image_name =  str(time.time())[:10]
            cv.imwrite(PATH_IMG + "\\" + image_name + ".jpg",frame)
            record(image_name)
            count_false = 0
        else:
            count_false += 1
        if count_false > 10:
            cap.release()
            break
        count+=1
        