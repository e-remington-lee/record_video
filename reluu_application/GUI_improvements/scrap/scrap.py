import numpy as np


a = np.zeros((1,5))
x = np.random.rand(1,5)
y = np.array([0.5, 0.1, 0, 0, 0])
z = np.array([0.5, 0.1, 0, 0, 0])
# print(x, y, z)
ad = np.add(a,z)
print(ad)