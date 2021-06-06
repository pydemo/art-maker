# rotate_image.py

"""
Image rotation using an OnSize event and a wx.bufferedDC.

Tested on Win7 64-bit (6.1.7600) and Win XP SP3 (5.1.2600)
Python 32-bit installed.

Platform  Windows 6.1.7600
Python    2.5.4 (r254:67916, Dec 23 2008, 15:10:54) [MSC v.1310 32 bit (Intel)]
Python wx 2.8.10.1
Pil       1.1.7

Ray Pasco      2010-06-09
pascor(at)verizon(dot)net

This code may be altered and/or distributed for any purpose whatsoever.
Use at you own risk. print (outs are suitable for framing or wrapping fish.
"""
import sys, os
import wx
import random       # set random rotation direction and to vary other settings
#import PIL.Image as Image       # Pil package for rotation+filtering all-in-one.

from PIL import Image

import ImgConv      # wxBitmap <==> wxImage <==> pilImage
#------------------------------------------------------------------------------

# What packages are installed ?
import sys, platform
print ()
print ( 'Platform ', platform.system())
if platform.system().lower() == 'windows' :
    print ( 'Windows  ', platform.win32_ver()[1])
print ( 'Python   ', sys.version)
print ( 'Wx       ', wx.VERSION_STRING)
print ( 'Pil      ', Image.__version__ )
print ()

#------------------------------------------------------------------------------

class DrawWindow( wx.Window ) :    # Window within the parent container.

    def __init__( self, parent=None, id=-1, imgFilename='defaultPngFilename' ) :
    
        wx.Window.__init__( self, parent=parent, id=id )
        
        self.imgFilename = imgFilename
        
        self.Bind( wx.EVT_SIZE, self.OnSize )           # For redraws other than on the timer events.
        self.Bind( wx.EVT_KEY_DOWN, self.OnKeyDown )
        
        self.Bind( wx.EVT_LEFT_DCLICK, self.OnDoubleClick )     # Change rotation direction
        
        self.Bind( wx.EVT_RIGHT_UP, self.OnRightUp )  # Quit the app
        
    #end def
    
    #------------------------
    
    def OnDoubleClick( self, event ):
        
        self.angleIncrement = 0.0 - self.angleIncrement
        event.Skip()
        
    #end def

    #------------------------
    
    def OnRightUp( self, event ):
        wx.Exit()
        event.Skip()
    #end def
        
    #------------------------
    
    def OnSize( self, event ) :
        self.DrawRotated( self.imgFilename )
        event.Skip() 
    #end def

    #------------------------
    
    def OnKeyDown( self, event ) :
        wx.Exit()                   # Easy way to end this program.  E.g., press the space-bar.
        event.Skip()
    #end def

    #------------------------
    
    def DrawRotated( self, imgFilename ) :
        
        clientWid, clientHgt = self.GetClientSize()
        bufferedDC = wx.BufferedDC( wx.ClientDC(self), wx.EmptyBitmap( clientWid, clientHgt ) )
        bufferedDC.SetBackground( wx.Brush( (220, 220, 240) ) )      # powder blue for .Clear()
        bufferedDC.Clear()                  # "Whitewash" over the previous drawing.
        
        try :                               # ? Have the local vars to be saved been created yet ?
            dummy = self.angle              # Try to access any one of the local vars.
            
        except :                            # No, so instantiate all the local variables only once:   
            self.angle = 0.0                # instantiate and initialize
            self.angleIncrement = 0.010     # heuristic value specified in radians for next timer event draw.
            self.direction = ( (random.randint( 0, 1 ) * 2) ) - 1       # Randomly either 0 or 1.
            self.angleIncrement *= self.direction               # 50% chance each of +1 or -1
            self.DEGREES_PER_RADIAN = 180.0 / 3.14159
            self.rotationCenterDummy = (0, 0)                   # has no effect in wx image rotation
            self.offsetAfterRotationDummy = wx.Point(100, 0)    # has no effect in wx image rotation
            self.readUsingPilOrWx = True
            self.drawCtr = 0
            
            self.pilImage = Image.open( imgFilename )
            self.wxImage  = wx.Image( imgFilename )
            
        #end try
        
        """
         Pil's  rotation .rotate() method enlarges the image just enough to hold the rotated image.
         The extended margins are completely transparent if the image has transparency (alpha).
         The alpha values can all be set to 255 (100% opaque) but the extended margins 
         will still be settransparent. This is the most reasonable way to extend an image 
         with any kind of transparency. (PNG, GIF and TIFF/TIF)
        
         Also, Pil rotation creates less image-to-image positioning jitter 
         when specifying the filter type to be "Image.BICUBIC". This needs more processing time.
         WX can also rotate and filter, but it must be done in 2 separate operations.
         Note that WX rotation specifies angles in degrees while Pil uses radians.
           
         Cropping the centered, rotated Pil image to the original image size is optionally done 
         by specifying "expand=False".
        
         The resultant image's outer edge aliasing (the "jaggies") needs to be addressed 
         equally with both rotation methods. (I left that to be done as an exercise.)
        """
        # Note that Pil's .rotate() is NOT an "in-place" method. E.g. :
        rotatedPilImage = self.pilImage.rotate( self.angle*self.DEGREES_PER_RADIAN, 
                                                Image.BICUBIC, expand=True )
        
        rotated_wxImage = ImgConv.WxImageFromPilImage( rotatedPilImage )  # Alpha is preserved
        #
        # The WX way (angle values are given in degrees).
        # The specified center-of-rotation and offset-after-rotation don't seem to have any effect.
        # Rotation image margins are set to black if .HasAlpha() is False.
        #
        #rotatedImage = wxImage.Rotate( self.angle, rotationCenterDummy, 
        #                               True, offsetAfterRotationDummy )
        # Insert a call to a wx filtering method here.
        
        # Center the rotated image on the client area.
        imageWid, imageHgt = rotated_wxImage.GetSize()
        offsetX = (clientWid - imageWid) / 2
        offsetY = (clientHgt - imageHgt) / 2
        # Display the rotated image. Only wxBitmaps can be displayed, not wxImages.
        # .DrawBitmap() autmatically "closes" the dc, meaning it finalizes the bitmap in some way.
        bufferedDC.DrawBitmap( rotated_wxImage.ConvertToBitmap(), offsetX, offsetY )
        
    #end def UpdateDrawing
    
#end class DrawWindow

#------------------------------------------------------------------------------

class TestFrame( wx.Frame ) :
    """Create a very simple app frame.
    This will be completely filled with the DrawWindow().
    """
    
    def __init__( self, imgFilename ) :
        
        self.runtimeMessage =  \
        """
        \n
        DOUBLE-CLICK ME TO CHANGE THE ROTATION DIRECTION.
        \n\n
        RIGHT-CLICK ME TO QUIT THIS DEMO.
        """
        
        wx.Frame.__init__( self, None, -1, 'Double Buffered Test',
                           pos=(0, 0), size=(700, 700) )
                           
        self.drawWindow = DrawWindow( self, -1, imgFilename )   # Instantiate
        self.imgFilename = imgFilename                          # Only for OnDrawTimer()
        
        # Set the frame size. Discard the opened pilImage afterward reading its size.
        pilImage = Image.open( imgFilename )
        imgSizeX, imgSizeY = pilImage.size
        clientSizeX = int( (1.414 * imgSizeX) + 25 )  # Max axis size necessary to completely show the rotated image
        clientSizeY = int( (1.414 * imgSizeY) + 25 )  # plus an arbitrary 25 pixel margin.
        maxSize = clientSizeX
        if clientSizeY > clientSizeX :    maxSize = clientSizeY
        self.SetClientSize( (maxSize, maxSize) )
            
        self.Show()                                 # The drawing window  must be shown before drawing.
        
        # Initial unrotated drawing. Subsequent timer events will call self.drawWindow.DrawRotated()
        # Subsequent draws will be incrementally rotated.
        self.drawWindow.DrawRotated( imgFilename )
        
        print ( self.runtimeMessage)
                                                    
        #---------------
        
        # Rotate the image and redisplay it every 50 milliseconds.
        self.drawTimer = wx.Timer( self, id=wx.NewId() )
        self.Bind( wx.EVT_TIMER, self.OnDrawTimer )
        self.drawTimer.Start( 50, oneShot=False )

    #end def __init__
    
    #--------------

    def OnDrawTimer( self, event ) :
        self.drawWindow.DrawRotated( self.imgFilename )             # The file is read in only once !
        self.drawWindow.angle += self.drawWindow.angleIncrement     # Adjust for the next .DrawRotated()
    #end def                                                        #  on the next timer tick.

#end class TestFrame

#------------------------------------------------------------------------------

if __name__ == '__main__' :

    inputFilename = 'STRIPES_ALPHA.PNG'     # Default filename when no given command-line filename.
    
    if len( sys.argv ) > 1 :    inputFilename = sys.argv[1]
    if not os.path.exists( inputFilename ) :
        print ( '\n####  Image Filename Not Found [ %s ]\n' % (inputFilename))
        os._exit(1)
    #end if

    myApp = wx.PySimpleApp( redirect=False )
    appFrame = TestFrame( inputFilename )     # TestFrame() must control when to .Show()
    myApp.MainLoop()

#end if

#------------------------------------------------------------------------------