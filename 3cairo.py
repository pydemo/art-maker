import wx 
import math


class myframe(wx.Frame):
    pt1 = 0
    pt2 = 0
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "test", size=(500,400))
        self.Bind(wx.EVT_LEFT_DOWN, self.onDown)
        self.Bind(wx.EVT_LEFT_UP, self.onUp)
        self.Bind(wx.EVT_PAINT, self.drawRect)

    def onDown(self, event):          
        global pt1
        pt1 = event.GetPosition() # firstPosition tuple

    def onUp(self, event):          
        global pt2
        pt2 = event.GetPosition() # secondPosition tuple

    def drawRect(self, event):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        nc = gc.GetNativeContext()
        ctx = Context_FromSWIGObject(nc)

        ctx.rectangle (pt1.x, pt1.y, pt2.x, pt2.y) # Rectangle(x0, y0, x1, y1)
        ctx.set_source_rgba(0.7,1,1,0.5)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.1,0.5,0)
        ctx.stroke()


app = wx.App()
f = myframe()
f.Show()
app.MainLoop()