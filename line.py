import wx
global coord
start=[10,10]
end = [30, 30]
class MyFrame(wx.Frame):
    """create a color frame, inherits from wx.Frame"""
    global coord
    def __init__(self, parent):
        # -1 is the default ID
        wx.Frame.__init__(self, parent, -1, "Click for mouse position", size=(400,300),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.SetBackgroundColour('Goldenrod')
        self.SetCursor(wx.StockCursor(wx.CURSOR_PENCIL))

        # hook some mouse events
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        #self.timer = wx.Timer(self)
        #self.timer.Start(1000) # fire every second
        #wx.CallAfter(1000, self.initDC)
        self.dc=None
    def onTimer(self, event):
        if not self.dc:
            self.initDC()
    def initDC(self):
        self.dc=dc = wx.PaintDC(self)
        #dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 4))    
    def OnLeftDown(self, event):
        global end
        """left mouse button is pressed"""
        pt = event.GetPosition()  # position tuple
        print (pt)
        end = [int(str(x)) for x in pt]
        self.SetTitle('LeftMouse = ' + str(pt))
        self.Refresh()

    def OnRightDown(self, event):
        global end
        """right mouse button is pressed"""
        pt = event.GetPosition()
        end = [int(str(x)) for x in pt]
        print (pt)

        self.SetTitle('RightMouse = ' + str(pt))
        self.Refresh()


    def OnPaint(self, event):
        global end, start
        if not self.dc:
            self.initDC()
        dc=self.dc
        #print(type(start), type(end))
        dc.DrawLine(*(start+end))
        start=end
        

app = wx.PySimpleApp()
frame = MyFrame(None)
frame.Show(True)
app.MainLoop()