import numpy as np
from struct import unpack
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

A = plt.imread("DeathValleyTif.tif")
fig, ax = plt.subplots()
ax.imshow(A,cmap=cm.gray)
ax.axis('off')

plt.show()
