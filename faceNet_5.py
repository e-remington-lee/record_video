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


import os
import threading

import cv2.cv2 as cv2
import PIL
import tensorflow as tf
import numpy as np

# def main(x,y,w,h, running):
#     try:
#         classifier.find_face()
#     except KeyboardInterrupt:
#         cv2.destroyAllWindows()  
#         tf.keras.backend.clear_session()
#         print("Ending session")

class FaceReader():
    debug = True
    running = False
    def __init__(self, x,y,w,h):
        threading.Thread.__init__(self)
        # self.begin_session_allocate_memory()
        self.model = tf.keras.models.load_model("faceNet\\xNet_noreg_v2_7202_best")
        self.path = "output\\"
        self.x = x
        self.y = y
        self.w = w
        self.h = h
         
    def run(self):
        try: 
            count = 1
            FaceReader.running = True
            while FaceReader.running:
                try:
                    img = PIL.ImageGrab.grab(bbox=(self.x,self.y,self.w,self.h))
                except OSError:
                    continue

                img = np.array(img)

                prediction = self.predict(img)
                print(prediction)
                
                if FaceReader.debug:
                    txt = prediction+"_predicted"+str(count)+".jpg"
                    im = PIL.Image.fromarray(img)
                    im.save(self.path+txt, "JPEG")
                    if count >= 200:
                        count = 1
                    count+=1
            cv2.destroyAllWindows()  

        except KeyboardInterrupt:
            cv2.destroyAllWindows()  
            tf.keras.backend.clear_session()
            print("Ending session")

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

    @staticmethod
    def stop_faceReader():
        FaceReader.running = False
    
    @staticmethod
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

def predict(model, image):
    size = 64
    # this line causes errors sometimes, unsure
    final_image = cv2.resize(image, (size,size))
    # final_image = tf.reshape(face, (size, size))
    
    final_image = np.expand_dims(final_image, 0)
    acc = model.predict([final_image])
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

def stop_faceReader():
    FaceReader.running = False


# FaceReader(10,10,50,50).find_face()