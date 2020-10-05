import numpy as np


a = np.zeros((1,5))
x = np.random.rand(1,5)
y = np.array([0.5, 0.1, 0, 0, 0])
z = np.array([[0.1, .6, 0.1, 0.1, 0.1]])
zz = np.array([[-1, 1, 0, -0.2, -0.2]])
x = np.multiply(z,zz)
xx = np.sum(x)
print(xx)