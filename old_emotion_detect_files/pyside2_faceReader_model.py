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
import multiprocessing

import cv2.cv2 as cv2
from PIL import ImageGrab, Image
import tflite_runtime.interpreter as tflite
# import tensorflow as tf
import numpy as np


class FaceReader():
    debug = True
    running = False
    
    def __init__(self, outputs_queue):
        # super(FaceReader, self).__init__()
        # self.begin_session_allocate_memory()
        # self.model = tf.keras.models.load_model("faceReader\\xNet_v3.2.0_SGD_128x128_8028_8063")
        import os 
        self.model = tflite.Interpreter("tflite_model\\optimized_model_v4.0.0_7779.tflite")
        self.path = "output\\"
        self.outputs_queue = outputs_queue
        self.front_face_cascade = cv2.CascadeClassifier("cascades\\haarcascade_frontalface_default.xml")
        self.emo = ""

    def run(self, x,y,w,h, count):
        try: 
            # redesign so there is another function that does the image grab and passes those locations back to model
            # image will only find location of face once every 10/20 to speed up performance
            try:
                img = ImageGrab.grab(bbox=(x,y,w,h))
                img = np.array(img)
                face = self.front_face_cascade.detectMultiScale(img, 1.1, 5, minSize=(30,30))
                if len(face) > 0:                
                    # crop face
                    for (x,y,w,h) in face:
                        cropped_face = img[y:y+h, x:x+w]
                        cropped_face = np.array(cropped_face)

                        if FaceReader.debug:
                            im = Image.fromarray(cropped_face)

                        cropped_face = cropped_face * 1.0/255
                        # perform 10-crop validation?                    
                        prediction = self.predict(cropped_face)
                        r_message = (prediction,)
                        self.outputs_queue.put(r_message)

                        if FaceReader.debug:
                            txt = self.emo+str(prediction)+"_predicted"+str(count)+".jpg"
                            im.save(self.path+txt, "JPEG")
                else:
                    if FaceReader.debug:
                        txt = f"No Face_{str(count)}+.jpg"
                        no_face = Image.fromarray(img)
                        no_face.save(self.path+txt, "JPEG")
                # Do I need this every loop?
                cv2.destroyAllWindows()
            except OSError or UnboundLocalError:
                pass
            
        except KeyboardInterrupt:
            cv2.destroyAllWindows()  
            print("Ending session")

    def predict(self, face):
        size = 80
        final_image = cv2.resize(face, (size,size))
        final_image = np.expand_dims(final_image, 0)
        
        # self.emo = ""
        # if result[0] > 0.3:
        #     self.emo += "anger_disgust" 
        # if result[1] > 0.3:
        #     self.emo += "joy"
        # if result[2] > 0.3:
        #     self.emo += "neutral" 
        # if result[3] > 0.3:
        #     self.emo += "sadness"
        # if result[4] > 0.3:
        #     self.emo += "surprise_fear"
        # if self.emo == "":
        #     self.emo = "No result"
        # acc = self.model.predict([final_image])
         # result = acc[0]

        self.model.allocate_tensors()

        # Get input and output tensors.
        input_details = self.model.get_input_details()
        output_details = self.model.get_output_details()

        # Test the model on random input data.
        # input_shape = input_details[0]['shape']
        input_data = np.array(final_image, dtype=np.float32)
        self.model.set_tensor(input_details[0]['index'], input_data)

        self.model.invoke()

        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
        result = self.model.get_tensor(output_details[0]['index'])

        self.emo = ""
        if result[0][0] > 0.3:
            self.emo += "anger_disgust" 
        if result[0][1] > 0.3:
            self.emo += "joy"
        if result[0][2] > 0.3:
            self.emo += "neutral" 
        if result[0][3] > 0.3:
            self.emo += "sadness"
        if result[0][4] > 0.3:
            self.emo += "surprise_fear"
        if self.emo == "":
            self.emo = "No result"

        return result[0]
    
    # @staticmethod
    # def begin_session_allocate_memory():
    #     tf.keras.backend.clear_session()
    #     tf.compat.v1.disable_eager_execution()
    #     gpus = tf.config.experimental.list_physical_devices('GPU')
    #     if gpus:
    #         try:
    #             for gpu in gpus:
    #                 tf.config.experimental.set_memory_growth(gpu, True)
    #         except RuntimeError as e:
    #             print(e)

