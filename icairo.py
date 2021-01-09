import wx
import cairo

class Canvas(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "test", pos=(0, 0), size=(640,480))
        #self.ShowFullScreen(1)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def DrawRectangle(self):
        pass

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        w,h = dc.GetSize()
        gc = wx.GraphicsContext.Create(dc)
        nc = gc.GetNativeContext()
        ctx = cairo.Context_FromSWIGObject(nc)


if __name__=="__main__":

    app = wx.App()
    canvas = Canvas()
    canvas.Show()
    app.MainLoop()