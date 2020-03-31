import wx

class MyPanel(wx.Panel):
    """ class MyPanel creates a panel to draw on, inherits wx.Panel """

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)

        self.SetBackgroundColour("white")
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        """set up the device context (DC) for painting"""
        dc = wx.PaintDC(self)

        #blue non-filled rectangle
        dc.SetPen(wx.Pen("blue"))
        dc.SetBrush(wx.Brush("blue", wx.TRANSPARENT)) #set brush transparent for non-filled rectangle
        dc.DrawRectangle(10,10,200,200)

        #red filled rectangle
        dc.SetPen(wx.Pen("red"))
        dc.SetBrush(wx.Brush("red"))
        dc.DrawRectangle(220,10,200,200)

app = wx.App()
frame = wx.Frame(None, -1, "Drawing A Rectangle...", size=(460, 300))
MyPanel(frame,-1)
frame.Show()        
frame.Centre()
app.MainLoop()