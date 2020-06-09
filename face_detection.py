import os
import zipfile
import random
import shutil
from shutil import copyfile
import cv2.cv2 as cv2

import tensorflow as tf
import numpy as np
import matplotlib as plt
from tensorflow.keras import layers
from tensorflow.keras import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image


def main():
    xyz = tf.keras.models.load_model("emotion_model.model")
    test_dir = "emotions/test/"
    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory(test_dir, target_size=(256,256), 
    batch_size=1, class_mode="categorical")
    xyz.evaluate(test_generator)

    Faces(xyz).find_face()

class Faces:
    def __init__(self, model):
        self.model = model

    
    def find_face(self):
        face_cascade = cv2.CascadeClassifier("hc.xml")
        path = "face_test/"
        cap = cv2.VideoCapture(0)
        count = 1
        while True:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
                face = gray[y:y+h, x:x+w]
                print(self.predict(face))
               
                # txt = "face_"+str(count)+".jpg"
                # cv2.imwrite(path+txt, face)
                # count += 1
                # if count > 300:
                #     count = 1

            cv2.imshow("img", img)
            k = cv2.waitKey(30)
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
    
    

    def predict(self, face):
        size = 256
        img_array = cv2.resize(face, (size,size))
        # print(img_array.shape)
        # image = np.expand_dims(img_array, axis=0)
        # image = np.expand_dims(img_array, axis=-1)
          
        image = img_array.reshape(-1, size,size,1)
        zeros = np.ones((1,1,1,3))
        fi = image*zeros
        acc = self.model.predict([fi])
        print(acc)
        return acc

main()