import numpy as np
from struct import unpack
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
#~ from matplotlib.path import Path
#~ from matplotlib.patches import PathPatch

datafile = open("DeathValleyTif.tif","rb")
s = datafile.read()
datafile.close()
h,w = 1800,1440

#~ A = np.array(unpack('h'*h*w,s[-(h*w*2):])).reshape((h,w))
A = np.frombuffer(s[-(h*w*2):], np.uint16).astype(float).reshape((w, h))
fig, ax = plt.subplots()
ax.imshow(A,cmap=cm.gray)
ax.axis('off')

plt.show()
