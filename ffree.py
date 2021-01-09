import wx
import math

class MainFrame(wx.Frame):
    """ Just a frame with a DrawPane """

    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(DrawPane(self), 1, wx.EXPAND)
        self.SetSizer(s)
        self.SetSize((1000, 1000))

########################################################################
class DrawPane(wx.PyScrolledWindow):
    """ A PyScrolledWindow with a 1000x1000 drawable area """

    VSIZE = (1000, 1000)

    def __init__(self, *args, **kw):
        wx.PyScrolledWindow.__init__(self, *args, **kw)
        self.SetScrollbars(10, 10, 1000, 1000)
        self.prepare_buffer()
        cdc = wx.ClientDC(self)
        self.PrepareDC(cdc)
        dc = wx.BufferedDC(cdc, self.buffer)
        #self.Draw(dc)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_down)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.radius=0
        self.delta=0.3
        self.pid=1

    def prepare_buffer(self):
        self.buffer = wx.EmptyBitmap(*DrawPane.VSIZE)
        cdc = wx.ClientDC(self)
        self.PrepareDC(cdc)
        dc = wx.BufferedDC(cdc, self.buffer)
        dc.Clear()
        dc.SetBackground(wx.Brush(wx.BLACK))
        dc.SetBackgroundMode(wx.TRANSPARENT)
        dc.DrawLine(0, 0, 999, 999) # Draw something to better show the flicker problem
        #dc.SetBackgroundMode(wx.SOLID)
        #dc.SetPen(wx.TRANSPARENT_PEN)

    def Draw(self, dc, scale=128):
        dc.Clear()
        width, height = dc.GetSize()
        sineTab = [
            int(127.5 * math.sin(math.pi * (i - 127.5) / 127.5) + 127.5)
            for i in range(256)
        ]
        cx = width / 8
        cy = height / 8
        bmp = wx.EmptyBitmap(width, height, 24)
        pixelData = wx.NativePixelData(bmp)
        pixels = pixelData.GetPixels()
        y = -cy
        for i in range(height):
            x = -cx
            for j in range(width):
                d = ((int(x) * int(x) + int(y) * int(y)) * scale) >> 8
                val = sineTab[d & 0xFF]
                pixels.Set(val, val, val)
                pixels.nextPixel()
                x += 1
            y += 1
            pixels.MoveTo(pixelData, 0, y + cy)
        dc.DrawBitmap(bmp, 0, 0, False) 
        
        
    def on_paint(self, evt):
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)

    def on_mouse_down(self, evt):
        self.mouse_pos = self.CalcUnscrolledPosition(evt.GetPosition()).Get()

    def on_motion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            newpos = self.CalcUnscrolledPosition(evt.GetPosition()).Get()
            coords = self.mouse_pos + newpos
            cdc = wx.ClientDC(self)
            self.PrepareDC(cdc)
            dc = wx.BufferedDC(cdc, self.buffer)
            pen = wx.Pen(wx.BLACK, 3)
            dc.SetPen(pen)
            #dc.SetBackgroundMode(wx.SOLID)
            #dc.SetPen(wx.TRANSPARENT_PEN)
            #dc.SetBackground(wx.Brush(wx.BLACK))
            dc.DrawLine(*coords)
            #print(coords[0])
            self.mouse_pos = newpos
            # Create graphics context from it
            gc = wx.GraphicsContext.Create(dc)
            #self.delta=0.2
            pens=[wx.RED_PEN,wx.BLUE_PEN,wx.YELLOW_PEN]
            pid=self.pid
            #print(pid,pid%len(pens))
            if gc:

                # make a path that contains a circle and some lines
                gc.SetPen(pens[pid%len(pens)])
                path = gc.CreatePath()
                if 0:
                    path.AddCircle(50.0, 50.0, 50.0)
                    path.MoveToPoint(0.0, 50.0)
                    path.AddLineToPoint(100.0, 50.0)
                    path.MoveToPoint(50.0, 0.0)
                    path.AddLineToPoint(50.0, 100.0)
                    path.CloseSubpath()
                    
                    path.AddRectangle(*(list(coords[:2]) + [50.0, 50.0]))
                path.AddCircle(*(list(coords[:2]) + [self.radius]))
                gc.StrokePath(path)

                self.radius +=self.delta
                if round(self.radius) ==100: self.delta =-self.delta
                if self.radius <0: 
                    self.delta = -self.delta
                    self.pid =self.pid+1
                #print(self.radius, round(self.radius),10)
                

if __name__ == "__main__":
    app = wx.PySimpleApp()
    wx.InitAllImageHandlers()
    MainFrame(None).Show()
    app.MainLoop()