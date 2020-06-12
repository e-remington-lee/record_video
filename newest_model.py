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

import tensorflow as tf
import numpy as np
from tensorflow.keras import layers
from tensorflow.keras import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image

# tf.config.gpu.set_per_process_memory_fraction(0.75)
# tf.config.gpu.set_per_process_memory_growth(True)
tf.keras.backend.clear_session()
tf.compat.v1.disable_eager_execution()
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
  except RuntimeError as e:
    print(e)

def main():  
    xyz = tf.keras.models.load_model("emotion_model.model")
    # test_dir = "production_test/"
    # test_datagen = ImageDataGenerator(rescale=1./255)
    # test_generator = test_datagen.flow_from_directory(test_dir, target_size=(256,256), 
    # batch_size=1, class_mode="categorical")
    # xyz.evaluate(test_generator)

    width, height = pyautogui.size()
    try:
        Faces(width, height, xyz).find_face()
    except KeyboardInterrupt:
        tf.keras.backend.clear_session()
        print("Ending session")

class Faces:
    def __init__(self, width, height, model):
        self.width = width
        self.height = height
        self.model = model

    
    def find_face(self):
        path = "./output/video"
        Path(path).mkdir(exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        screen_size = (self.width, self.height)
        out = cv2.VideoWriter(path+"/output.avi", fourcc, 20.0, (screen_size))

        face_cascade = cv2.CascadeClassifier("hc.xml")

        count = 1          
        while True:

            img = pyautogui.screenshot()
            img = np.array(img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  
            out.write(img)

            # face_detected = False
            # if not face_detected:
            #     print("-----face not detected------")

            for (x,y,w,h) in faces:
                # face_detected = True
                # if face_detected:
                #     print("---detected face!---")

                cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
                face = gray[y:y+h, x:x+w]
                print(self.predict(face))
                txt = "clip_"+str(count)+".jpg"
                cv2.imwrite(path + txt, img)

                if count >= 1000:
                    count = 1
                count+=1


            k = cv2.waitKey(30)
            if k == 27:
                break

        out.release()
        cv2.destroyAllWindows()   
    

    def predict(self, face):
        size = 256
        img_array = cv2.resize(face, (size,size))
      
        image = img_array.reshape(-1, size,size,1)
        zeros = np.ones((1,1,1,3))
        fi = image*zeros
        acc = self.model.predict([fi])
        print(acc)
        return acc

main()