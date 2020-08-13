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

class FaceReader(multiprocessing.Process):
    debug = True
    running = False
    def __init__(self, x,y,w,h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
         
    def run(self):
        while True:
            x = self.predict(self.x,self.y,self.w,self.h)
            print(x)
            print("idk")
        

    def predict(self, x,y,w,h):
        return x,y,w,h

def stop_faceReader():
    FaceReader.running = False


# FaceReader(10,10,50,50).find_face()