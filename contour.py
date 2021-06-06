import sys

import wx

from numpy import exp, random, arange, outer
from wxmplot import ImageFrame

def gauss2d(x, y, x0, y0, sx, sy):
    return outer(exp(-(((y-y0)/float(sy))**2)/2),
                 exp(-(((x-x0)/float(sx))**2)/2))

ny, nx = 350, 400
x = arange(nx)
y = arange(ny)
ox =  x / 62.
oy = -2 + y / 97.0
dat = 0.2 + (0.3*random.random(size=nx*ny).reshape(ny, nx) +
             6.0*gauss2d(x, y, 90,   76,  5,  6) +
             1.0*gauss2d(x, y, 180, 100,  7,  3) +
             1.0*gauss2d(x, y, 175,  98,  3,  7) +
             0.5*gauss2d(x, y, 181,  93,  4, 11) +
             1.8*gauss2d(x, y, 270, 230, 78, 63) +
             0.9*gauss2d(x, y, 240, 265,  8,  3) +
             7.0*gauss2d(x, y, 40,  310,  2,  3) )


app = wx.App()
frame = ImageFrame(mode='intensity')
frame.display(dat, x=ox, y=oy)
frame.Show()
app.MainLoop()