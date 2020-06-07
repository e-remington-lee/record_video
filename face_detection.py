import cv2.cv2 as cv2
import numpy as np


def main():
    Faces.find_face()

class Faces:

    @staticmethod
    def find_face():
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
                txt = "face_"+str(count)+".jpg"
                cv2.imwrite(path+txt, face)
                count += 1
                if count > 300:
                    count = 1

            cv2.imshow("img", img)
            k = cv2.waitKey(30)
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

main()