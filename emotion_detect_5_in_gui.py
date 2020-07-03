#    Copyright 2020 Erik Lee

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


from pathlib import Path
import os
import cv2.cv2 as cv2
import pyautogui
import PIL

import tensorflow as tf
import numpy as np

def main(x,y,w,h):
    debug = True
    begin_session_allocate_memory()
    model = tf.keras.models.load_model("faceNet\\xNet_noreg_v2_7202_best")

    width, height = pyautogui.size()
    path = "output/"
    out = None
    if debug:
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        screen_size = (width, height)
        out = cv2.VideoWriter(path+"video/output.avi", fourcc, 20.0, (screen_size))
    Path(path).mkdir(exist_ok=True)
    
    classifier = Faces(width, height, model, path, out, x,y,w,h)
    try:
        classifier.find_face()
    except KeyboardInterrupt:
        if out:
            out.release()
        cv2.destroyAllWindows()  
        tf.keras.backend.clear_session()
        print("Ending session")

class Faces:
    def __init__(self, width, height, model, path, out, x,y,w,h):
        self.width = width
        self.height = height
        self.model = model
        self.path = path
        self.out = out
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.face_detected = False  
        
    
    def find_face(self):
        front_face_cascade = cv2.CascadeClassifier("cascades\haarcascade_frontalface_default.xml")

        count = 1
        while True:
            try:
                # img = pyautogui.screenshot()
                img = PIL.ImageGrab.grab(bbox=(self.x,self.y,self.w,self.h))
            except OSError:
                continue

            img = np.array(img)
            faces = front_face_cascade.detectMultiScale(img, 1.1, 5, minSize=(30,30))
            if self.out:
                self.out.write(img)

            if len(faces) > 0:
                self.face_detected = True
                for (x,y,w,h) in faces:
                    # if self.out:
                    #     cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 1)
                    # TODO increase the face capture size? or not
                    # TODO try/except and catch the error that crashes the program if the face is less than 70
                    face = img[y:y+h, x:x+w]
                    prediction = self.predict(face)
                    print(prediction)
                    
                    if self.out:
                        txt = prediction+"_predicted"+str(count)+".jpg"
                        # cv2.imwrite(self.path + txt, face)
                        im = PIL.Image.fromarray(face)
                        im.save(self.path+txt, "JPEG")
                        if count >= 200:
                            count = 1
                        count+=1
                   
            else:
                self.face_detected = False
                print("-----face not detected------")

        if self.out:
            self.out.release()
        cv2.destroyAllWindows()  


    def predict(self, face):
        size = 64
        # this line causes errors sometimes, unsure
        final_image = cv2.resize(face, (size,size))
        # final_image = tf.reshape(face, (size, size))
      
        final_image = np.expand_dims(final_image, 0)
        acc = self.model.predict([final_image])
        output = ""
        result = acc[0]

        if result[0] > 0.5:
            output += "anger_disgust"
        if result[1] > 0.5:
            output += "joy"
        if result[2] > 0.5:
            output += "neutral" 
        if result[3] > 0.5:
            output += "sadness"
        if result[4] > 0.5:
            output += "surprise_fear"
        if output == "":
            output = "No result"

        return output


def begin_session_allocate_memory():
    tf.keras.backend.clear_session()
    tf.compat.v1.disable_eager_execution()
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(e)
