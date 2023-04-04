import cv2
import torch
import numpy as np
from time import sleep
from threading import Thread

class VideoCamera:

    def __init__(self, src=0):
        if src == 0:
            self.cap = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        else:
            self.cap = cv2.VideoCapture(src)
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/epochs_100/weights.pt')
        self.ret, self.frame = self.cap.read()
        self.result_frame = None

        self.t = Thread(target=self.prediction, args=[self.frame])
        self.t.daemon = True
        self.t.start()

    def __del__(self):
        self.cap.release()

    def prediction(self, frame):
        result = self.model(frame)
        self.result_frame = np.squeeze(result.render())
    
    def get_frame(self):
        self.ret, self.frame = self.cap.read()

        if self.frame is None:
            return

        self.prediction(self.frame)

        return self.result_frame 
