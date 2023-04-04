import os
from django.shortcuts import render, redirect 
from core.models import Alert, FileUpload
from django.conf import settings
from django.http import StreamingHttpResponse
from core.camera import VideoCamera
from time import time, sleep
import torch
import cv2
import numpy as np

def index(request):

    if request.method == 'POST':
        
        name = request.POST.get('name')
        file = request.FILES.get('file')

        fileUpload = FileUpload.objects.create(name=name,
                                               file=file)
        fileUpload.save()
        return redirect('index')
    
    data = FileUpload.objects.all()
    context = {"data":data} 
    
    return render(request, 'index.html', context)

def deleteSample(request, pk):
    file = FileUpload.objects.get(id=pk)
    file_name = file.file.name
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    os.remove(file_path)
    file.delete()
    return redirect('index')

def alertsList(request):
    alerts = Alert.objects.all()
    context = {"alerts":alerts}
    return render(request, 'alerts.html', context)

def videoFrame(camera):

    prev_frame_time = 0
    new_frame_time = 0
    prev_counts = {}

    while True:
        
        try:
            image = camera.get_frame()
        except TypeError:
            return redirect('index')
        
        new_frame_time = time()
        try:
            fps = int(1 / (new_frame_time - prev_frame_time))
        except ZeroDivisionError:
            fps = 0
        
        res_img = cv2.putText(image, f'FPS: {fps}', (50,100), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0,255,0), 2, cv2.LINE_AA)
        _, jpeg = cv2.imencode('.jpg', res_img)
        frame = jpeg.tobytes()

        prev_frame_time = new_frame_time

        if not frame:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def stream(request, pk):
    file = FileUpload.objects.get(id=pk)
    file_name = file.file.name
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    camera = VideoCamera(src=file_path)
    yields = videoFrame(camera)
    return StreamingHttpResponse(yields,
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def show(request):
    return render(request, 'sample.html')
