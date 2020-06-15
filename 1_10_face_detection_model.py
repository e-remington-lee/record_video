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
import pyscreenshot as ImageGrab

import tensorflow as tf
import numpy as np
from tensorflow.keras import layers
from tensorflow.keras import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image

# tf.config.gpu.set_per_process_memory_fraction(0.75)
# tf.config.gpu.set_per_process_memory_growth(True)

def main():
 

    debug = True
    begin_session_allocate_memory()
    model = tf.keras.models.load_model("emotion_model_v1.0_realfaces.model")

    width, height = pyautogui.size()
    path = "./output/video"
    out = None
    if debug:
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        screen_size = (width, height)
        out = cv2.VideoWriter(path+"/output.avi", fourcc, 20.0, (screen_size))
    Path(path).mkdir(exist_ok=True)
    
    classifier = Faces(width, height, model, path, out)
    try:
        classifier.find_face()
    except KeyboardInterrupt:
        if out:
            out.release()
        cv2.destroyAllWindows()  
        tf.keras.backend.clear_session()
        print("Ending session")

class Faces:
    def __init__(self, width, height, model, path, out):
        self.width = width
        self.height = height
        self.model = model
        self.path = path
        self.out = out
        self.face_detected = False  
        
    
    def find_face(self):
        front_face_cascade = cv2.CascadeClassifier("cascades\haarcascade_frontalface_default.xml")

        count = 1
        while True:
            try:
                img = pyautogui.screenshot()
            except OSError:
                continue

            img = np.array(img)
            faces = front_face_cascade.detectMultiScale(img, 1.3, 5, minSize=(40,40))
            
            if len(faces) > 0:
                save_time = 0
                while save_time < 10:
                    self.face_detected = True
                    for (x,y,w,h) in faces:
                        # cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
                        # face = img[y:y+h, x:x+w]
                        face = ImageGrab.grab(bbox=(x-50,y-50,x+h+50,y+h+50))
                        face = np.array(face)
                        if self.out:
                                self.out.write(face)
                        print(self.predict(face))
                        
                        if self.out:
                            txt = "clip_"+str(count)+".jpg"
                            cv2.imwrite(self.path + txt, face)
                            if count >= 1000:
                                count = 1
                            count+=1
                    save_time+=1
            else:
                self.face_detected = False
                print("-----face not detected------")

        if self.out:
            self.out.release()
        cv2.destroyAllWindows()  


    def predict(self, face):
        size = 256
        final_image = cv2.resize(face, (size,size))
      
        final_image = np.expand_dims(final_image, 0)
        acc = self.model.predict([final_image])
        output = ""
        result = acc[0]

        if result[0] > 0.5:
            output += "angry"
        if result[1] > 0.5:
            output += "disgust"
        if result[2] > 0.5:
            output += "fear"
        if result[3] > 0.5:
            output += "joy"
        if result[4] > 0.5:
            output += "neutral"
        if result[5] > 0.5:
            output += "sadness"
        if result[6] > 0.5:
            output += "surprise"
        if output == "":
            output = "No result"

        return output


def begin_session_allocate_memory():
    tf.keras.backend.clear_session()
    tf.compat.v1.disable_eager_execution()
    gpus = tf.config.experimental.list_physical_devices('GPU')
    cpus = tf.config.experimental.list_physical_devices('CPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(e)
    else:
        try:
            for cpu in cpus:
                tf.config.experimental.set_memory_growth(cpu, True)
        except RuntimeError as e:
            print(e)

main()