import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
#~ image = plt.imread("rgb320x320.tif")

image = np.arange(0,1,1/400).reshape((20,20))
image[5:10,2:6] = 1
#~ plt.figure(figsize=(4,4),dpi=72)
plt.rcParams["figure.figsize"]=(10,10)
fig, ax = plt.subplots()
ax.imshow(image,cmap=cm.gray,interpolation='none')
ax.axis('off')

plt.show()
