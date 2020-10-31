'''
This files parses the full videoes to the segmented ones. We do this so the labels in the open_face.csv match what we have
'''
import os
import sys
import csv 
import h5py
import numpy as np
import pandas as pd
import pickle

from PIL import Image
import cv2
import numpy as np
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

dataset_path = 'D:/Software/reluu_extra_space/CMU_MOSEI/Raw/Videos/Full/Combined'
save_video_dir = 'D:/Software/reluu_extra_space/CMU_MOSEI/Raw/Videos/new_segmented'
with open("mosei_labels.csv") as csvfile:
    csvfile = csv.reader(csvfile, delimiter=",")
    next(csvfile)
    for row in csvfile:
        full_video = f"{row[1]}.mp4"
        segmented_video = f"{row[2]}.mp4"
        video_path = os.path.join(dataset_path, full_video)
        save_video_path = os.path.join(save_video_dir, segmented_video)
        # print(row[4], row[5])
        ffmpeg_extract_subclip(video_path, float(row[4]), float(row[5]), targetname=save_video_path)
        # print(video_path)
        # print(save_video_path)