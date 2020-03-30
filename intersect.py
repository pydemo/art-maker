# Click on the window to draw a line.
# The program will tell you if this and the other line intersect.

import wx

class Point:
    def __init__(self, newX, newY):
        self.x = newX
        self.y = newY

app = wx.App()
frame = wx.Frame(None, wx.ID_ANY, "Main")
p1 = Point(90,200)
p2 = Point(150,80)
mp = Point(0,0) # mouse point
highestX = 0


def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def is_intersection(p1, p2, p3, p4):
    return intersect(p1, p2, p3, p4)

def drawIntersection(pc):
    mp2 = Point(highestX, mp.y)
    if is_intersection(p1, p2, mp, mp2):
        pc.DrawText("intersection", 10, 10)
    else:
        pc.DrawText("no intersection", 10, 10)

def do_paint(evt):
    pc = wx.PaintDC(frame)
    pc.DrawLine(p1.x, p1.y, p2.x, p2.y)
    pc.DrawLine(mp.x, mp.y, highestX, mp.y)
    drawIntersection(pc)

def do_left_mouse(evt):
    global mp, highestX
    point = evt.GetPosition()
    mp = Point(point[0], point[1])
    highestX = frame.Size[0]
    frame.Refresh()

frame.Bind(wx.EVT_PAINT, do_paint)
frame.Bind(wx.EVT_LEFT_DOWN, do_left_mouse)
frame.Show()
app.MainLoop()