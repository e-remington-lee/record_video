import os
import zipfile
import random
import shutil
from shutil import copyfile

parent_path = "FERG_DB_256"

def main():
    Label().label_data(parent_path)

class Label():
    def __init__(self):
        self.anger = "emotions/anger/"
        self.disgust = "emotions/disgust/"
        self.fear = "emotions/fear/"
        self.joy = "emotions/joy/"
        self.neutral = "emotions/neutral/"
        self.sadness = "emotions/sadness/"
        self.surprise = "emotions/surprise/"

    def label_data(self, parent_path):
        list_dir = os.listdir(parent_path)
        for name in list_dir:
            # Example: "FERG_DB_256/aia"
            p = os.path.join(parent_path, name)
            if os.path.isdir(os.path.join(p)):
                for x in os.listdir(p):
                    # Example: "FERG_DB_256/aia/anger"   
                    final_dir = os.path.join(p,x)
                    if "anger" in x and os.path.isdir(final_dir):
                        self.copy_files(final_dir, self.anger)
                    elif "disgust" in x and os.path.isdir(final_dir):
                        self.copy_files(final_dir, self.disgust)
                    elif "fear" in x and os.path.isdir(final_dir):
                        self.copy_files(final_dir, self.fear)
                    elif "joy" in x and os.path.isdir(final_dir):
                        self.copy_files(final_dir, self.joy)
                    elif "neutral" in x and os.path.isdir(final_dir):
                        self.copy_files(final_dir, self.neutral)
                    elif "sadness" in x and os.path.isdir(final_dir):
                        self.copy_files(final_dir, self.sadness)
                    elif "surprise" in x and os.path.isdir(final_dir):
                        self.copy_files(final_dir, self.surprise)
                    else:
                        continue

    def copy_files(self, final_dir, anger):
        for pic in os.listdir(final_dir):
            file_ = os.path.join(final_dir, pic)
            dest_ = os.path.join(anger, pic)
            if os.path.getsize(file_) != 0:
                print(os.getcwd())
                copyfile(file_, dest_)
    
if __name__ == "__main__":
    main()