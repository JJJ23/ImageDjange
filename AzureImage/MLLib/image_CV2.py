from django.shortcuts import render
#from .forms import FaceAdditionForm
import cv2
import numpy as np
from django.http import StreamingHttpResponse

'''
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
    def __del__(self):
        self.video.release()
    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

'''