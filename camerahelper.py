from flask import Flask, render_template, Response
from keras.models import load_model

import numpy as np
import cv2


# load model
model = load_model("best_model.h5")

class_to_label = {0 :'Angry', 1 : 'Disgust', 2:'Fear', 3 :'Happy', 4:'Sad', 5:'Surprise', 6:'Neutral'}
camera = cv2.VideoCapture(0)  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
            res, frame = camera.read()  # read the camera frame
            if res == False:
                continue
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
            faces = face_cascade.detectMultiScale(frame,1.2,5)
            

            
            if len(faces)  == 0:
                for (x,y,w,h) in faces:
                    cv2.putText(frame, "Processing", (x,y-10), cv2.FONT_HERSHEY_COMPLEX,1,(255,30,0),2,cv2.LINE_AA)

                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        

            for face in faces:
                x,y,w, h = face
                
                offset = 10
                face_section = gray_frame[y-offset:y+h+offset,x-offset:x+w+offset]
                
                if(np.all(np.array(face_section.shape))):
                    face_section = cv2.resize(face_section,(48,48))

                    pred = np.argmax(model.predict(face_section.reshape(1,48,48,1)))
                    label = class_to_label[pred]

                    cv2.putText(frame, label, (x,y-10), cv2.FONT_HERSHEY_COMPLEX,1,(255,30,0),2,cv2.LINE_AA)
                    cv2.rectangle(frame,(x,y),(x+w,y+h), (0,255,255),2)


            ret, jpeg = cv2.imencode('.jpg', frame)
            data = []
            data.append(jpeg.tobytes())
            #data.append(label)
            return data
