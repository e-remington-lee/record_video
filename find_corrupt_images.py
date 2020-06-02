from PIL import Image
import os

path = "emotions/test/surprise"
li = os.listdir(path)
print(path)
for x in li:
    p = os.path.join(path, x)
    Image.open(p)