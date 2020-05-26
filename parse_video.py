import cv2
import imutils as utils


vc = cv2.cv2.VideoCapture("./video_original/btb.mp4")
count = 1
success = True

while success:
    success, frame = vc.read()
    # frame = utils.rotate_bound(frame, 90)
    txt = "clip_"+str(count)+".jpg"
    cv2.cv2.imwrite("./video_frames/" + txt, frame)
    count +=1
    if count > 1000:
        break
vc.release()
