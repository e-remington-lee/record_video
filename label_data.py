import os
import zipfile
import random
import shutil
from shutil import copyfile

parent_path = "FERG_DB_256"

def main():
    Label().delete_files("emotions")
    Label().label_data(parent_path)

class Label():
    def __init__(self, train="emotions/train/", test="emotions/test/", validation="emotions/validation/"):
        self.train = train
        self.test = test
        self.validation = validation
        self.anger = "anger"
        self.disgust = "disgust"
        self.fear = "fear"
        self.joy = "joy"
        self.neutral = "neutral"
        self.sadness = "sadness"
        self.surprise = "surprise"
        self.train_test_split = 0.8

    def label_data(self, parent_path):
        list_dir = os.listdir(parent_path)
        for name in list_dir:
            # Example: "FERG_DB_256/aia"
            p = os.path.join(parent_path, name)
            if os.path.isdir(os.path.join(p)):
                for x in os.listdir(p):
                    # Example: "FERG_DB_256/aia/anger"   
                    final_dir = os.path.join(p,x)
                    if self.anger in x and os.path.isdir(final_dir):
                        self.copy_files(final_dir, self.anger)
                    elif self.disgust in x and os.path.isdir(final_dir):
                        self.copy_files(final_dir, self.disgust)
                    elif self.fear in x and os.path.isdir(final_dir):
                        self.copy_files(final_dir, self.fear)
                    elif self.joy in x and os.path.isdir(final_dir):
                        self.copy_files(final_dir, self.joy)
                    elif self.neutral in x and os.path.isdir(final_dir):
                        self.copy_files(final_dir, self.neutral)
                    elif self.sadness in x and os.path.isdir(final_dir):
                        self.copy_files(final_dir, self.sadness)
                    elif self.surprise in x and os.path.isdir(final_dir):
                        self.copy_files(final_dir, self.surprise)
                    else:
                        continue

    def copy_files(self, final_dir, emotion, percent=0.6):
        # Speed up training just use less data
        full_dir = os.listdir(final_dir)
        random.shuffle(full_dir)
        length = int(len(full_dir)*percent)
        list_dir = full_dir[0:length]

        split_size = int(len(list_dir)*self.train_test_split)
        train = list_dir[0:split_size]

        #create test and validation directories
        test_and_validation = list_dir[split_size:]
        test_and_validation_length = int(len(test_and_validation))

        test = test_and_validation[:test_and_validation_length//2]
        validation = test_and_validation[test_and_validation_length//2:]

        for pic in train:
            file_ = os.path.join(final_dir, pic)
            emotion_dir = os.path.join(self.train, emotion)
            dest_ = os.path.join(emotion_dir, pic)
            if os.path.getsize(file_) != 0:
                copyfile(file_, dest_)

        for pic in test:
            file_ = os.path.join(final_dir, pic)
            emotion_dir = os.path.join(self.test, emotion)
            dest_ = os.path.join(emotion_dir, pic)          
            if os.path.getsize(file_) != 0:
                copyfile(file_, dest_)

        for pic in validation:
            file_ = os.path.join(final_dir, pic)
            emotion_dir = os.path.join(self.validation, emotion)
            dest_ = os.path.join(emotion_dir, pic)          
            if os.path.getsize(file_) != 0:
                copyfile(file_, dest_)

    def delete_files(self, mypath):
        for root, dirs, files in os.walk(mypath):
            for x in files:
                os.remove(os.path.join(root, x))
    
if __name__ == "__main__":
    main()