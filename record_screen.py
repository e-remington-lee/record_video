
from pathlib import Path

import cv2
import numpy as np
import pyautogui

def main():
    width, height = pyautogui.size()
    Record(width, height, True).record_screen()

class Record():
    def __init__(self, width, height, video=False):
        self.width = width
        self.height = height
        self.video = video

    def record_screen(self):
        Path("./output").mkdir(exist_ok=True)

        if self.video:
            path = "./output/video"
            Path(path).mkdir(exist_ok=True)

            fourcc = cv2.cv2.VideoWriter_fourcc(*"XVID")
            # # create the video write object
            screen_size = (self.width, self.height)
            out = cv2.cv2.VideoWriter(path+"/output.avi", fourcc, 20.0, (screen_size))

        count = 1
        while True:
            path = "./output/screen_record_frames/"
            Path(path).mkdir(parents=True, exist_ok=True)
            
            # make a screenshot
            img = pyautogui.screenshot()
            # img = pyautogui.screenshot(region=(0, 0, 300, 400))
            # convert these pixels to a proper numpy array to work with OpenCV
            frame = np.array(img)
            # convert colors from BGR to RGB
            frame = cv2.cv2.cvtColor(frame, cv2.cv2.COLOR_BGR2RGB)

            #writes the frame
            txt = "clip_"+str(count)+".jpg"
            cv2.cv2.imwrite(path + txt, frame)

            if count >= 300:
                count = 1
            count+=1

            # write the frame
            if self.video:
                out.write(frame)

            #show the frame
            cv2.cv2.imshow("screenshot", frame)

            # if the user clicks q, it exits

            if cv2.cv2.waitKey(1) == ord("q"):
                break

        # make sure everything is closed when exited
        cv2.cv2.destroyAllWindows()
        out.release()
        
if __name__== "__main__":
   main()
