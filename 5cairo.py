#!/usr/bin/python

import wx
import wx.lib.wxcairo
import cairo

class DrawingArea(wx.Panel):
    
    def __init__ (self , *args , **kw):
        super(DrawingArea , self).__init__ (*args , **kw)
        
        self.SetDoubleBuffered(True)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnPaint(self, e):
        
        dc = wx.PaintDC(self)
        cr = wx.lib.wxcairo.ContextFromDC(dc)
        self.DoDrawing(cr)     
        
    def DoDrawing(self, cr):
        
        cr.set_source_rgb (0.2 , 0.23 , 0.9)
        cr.rectangle(10 , 15, 90, 60)
        cr.fill()
        
        cr.set_source_rgb(0.9 , 0.1 , 0.1)
        cr.rectangle(130 , 15, 90, 60)
        cr.fill()
        
        cr.set_source_rgb(0.4 , 0.9 , 0.4)
        cr.rectangle(250 , 15, 90, 60)       
        cr.fill()     


class Frame(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Frame, self).__init__(*args, **kwargs) 
        
        self.InitUI()

    def InitUI(self):
        #----------------------------------------------------
        # Build menu bar and submenus   
        
        menubar = wx.MenuBar()
        # file menu containing quit menu item
        fileMenu = wx.Menu() 
        quit_item = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        fileMenu.AppendItem(quit_item)
        self.Bind(wx.EVT_MENU, self.OnQuit, quit_item)
        menubar.Append(fileMenu, '&File')      

        # help menu containing about menu item
        helpMenu = wx.Menu() 
        about_item = wx.MenuItem(helpMenu, wx.ID_ABOUT, '&About\tCtrl+A')
        helpMenu.AppendItem(about_item)
        #~ self.Bind(wx.EVT_MENU, self.OnAboutBox, about_item)
        menubar.Append(helpMenu, '&Help')     

        self.SetMenuBar(menubar)

        #----------------------------------------------------
        # Build window layout

        panel = wx.Panel(self)        
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)        

        midPan = DrawingArea(panel)
        vbox.Add(midPan, 1, wx.EXPAND | wx.ALL, 12)
    

        smallPan = wx.Panel(panel)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(smallPan, 1, wx.EXPAND|wx.ALL, 12)
        smallPan.SetSizer(hbox2)   

        #----------------------------------------------------
        # Place buttons in correct box corresponding with panel

        close_button = wx.Button(smallPan, wx.ID_CLOSE)
        self.Bind(wx.EVT_BUTTON, self.OnQuit, close_button)

        hbox2.Add(close_button)
        
        #----------------------------------------------------
        # Set window properties

        #~ self.SetSize((1600, 1200))
        self.SetSize((400, 250))
        #~ self.Maximize()
        self.SetTitle('PROGRAM NAME')
        self.Centre()

    def OnQuit(self, e):
        self.Close()

def main():
    ex = wx.App()
    f = Frame(None)
    f.Show(True)  
    ex.MainLoop()  

if __name__ == '__main__':
    main()