from numpy import arange, sin, pi
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

import wx

import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector

#fig, ax = plt.subplots()

def onSelect(x):
    print(x)

def onPress(event):
    print('Mouse pressed')

def onRelease(event):
    print('Mouse released')
if 0:
    lineprops = {'color': 'red', 'linewidth': 4, 'alpha': 0.8}
    lsso = LassoSelector(ax=ax, onselect=onSelect, lineprops=lineprops)

    fig.canvas.mpl_connect('button_press_event', onPress)
    fig.canvas.mpl_connect('button_release_event', onRelease)

    plt.show()
    plt.show()



class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def draw(self):
        if 0:
            t = arange(0.0, 3.0, 0.01)
            s = sin(2 * pi * t)
            self.axes.plot(t, s)
        lineprops = {'color': 'red', 'linewidth': 4, 'alpha': 0.8}
        self.lsso = LassoSelector(ax=self.axes, onselect=onSelect, lineprops=lineprops)
        self.canvas.mpl_connect('button_press_event', onPress)
        self.canvas.mpl_connect('button_release_event', onRelease)
        plt.show()

if __name__ == "__main__":
    app = wx.PyApp()
    fr = wx.Frame(None, title='test')
    panel = CanvasPanel(fr)
    panel.draw()
    fr.Show()
    app.MainLoop()
    
    
    