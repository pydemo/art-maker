import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector
from matplotlib import path

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax1.set_title('lasso selection:')
ax1.plot()
ax1.set_xlim([0, 10])
ax1.set_ylim([0, 10])
ax1.set_aspect('equal')

# Empty array to be filled with lasso selector
array = np.zeros((10,10))
ax2 = fig.add_subplot(122)
ax2.set_title('numpy array:')
msk = ax2.imshow(array, origin='lower',vmax=1, interpolation='nearest')
ax2.set_xlim([-1, 10])
ax2.set_ylim([-1, 10])

# Pixel coordinates
pix = np.arange(10)
xv, yv = np.meshgrid(pix,pix)
pix = np.vstack( (xv.flatten(), yv.flatten()) ).T

def updateArray(array, indices):
    lin = np.arange(array.size)
    newArray = array.flatten()
    newArray[lin[indices]] = 1
    return newArray.reshape(array.shape)

def onselect(verts):
    global array, pix
    p = path.Path(verts)
    ind = p.contains_points(pix, radius=1)
    array = updateArray(array, ind)
    msk.set_data(array)
    fig.canvas.draw_idle()

lasso = LassoSelector(ax1, onselect)

plt.show()