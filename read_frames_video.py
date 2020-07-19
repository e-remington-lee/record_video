import cv2
li = ["1001_IEO_FEA_MD.flv", "1001_IEO_HAP_HI.flv", "1001_IEO_HAP_LO.flv"]

for x in li:
    vidcap = cv2.VideoCapture(x)
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(f"frame{count}.jpg", image)     # save frame as JPEG file      
        success,image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1