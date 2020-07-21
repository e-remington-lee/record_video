import numpy as numpy
import time
from PIL import Image


# a1 = [0.6, 0.7, 0.1]
# a2 = [0.3, 0.6, 0.1]

# n1 = numpy.array(a1)
# n2 = numpy.array(a2)

# x = numpy.add(n1, n2) / 2

# a = numpy.empty(10, dtype=object)


pi = numpy.asarray(Image.open("emotions_5\\test\\anger_disgust\\AF03ANHL.JPG"))
print(pi.shape)

