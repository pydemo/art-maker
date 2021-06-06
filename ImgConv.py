# ImgConv.py

"""
Based on pyWiki 'Working With Images' @  http://wiki.wxpython.org/index.cgi/WorkingWithImages
Modified to properly copy, create or remove any alpha in all input/output permutations.

Tested on Win7 64-bit (6.1.7600) and Win XP SP3 (5.1.2600) using an AMD Athlon AM2 processor. 
Python 32-bit installed.

Platform  Windows 6.1.7600
Python    2.5.4 (r254:67916, Dec 23 2008, 15:10:54) [MSC v.1310 32 bit (Intel)]
Python wx 2.8.10.1
Pil       1.1.7

Ray Pasco      2010-06-09
pascor(at)verizon(dot)net

This code may be altered and/or distributed for any purpose whatsoever.
Use at you own risk. Printouts are suitable for framing or wrapping fish.
"""
import os
import wx       # WxBmap <==> wxImage
import PIL.Image    # wxImage <==> PilImage. # Needed only if you convert to or from Pil image formats
from pprint import pprint as pp
#------------------------------------------------------------------------------

#   image type      image type     image type
#       1                2              3
#    wxBmap   <==>    wxImage  <==>  pilImage

def WxImageFromWxBitmap( wxBmap ) :              # 1 ==> 2
    return wx.ImageFromBitmap( wxBmap )
#end def

def PilImageFromWxBitmap( wxBmap ) :             # 1 ==> 3
    return PilImageFromWxImage( WxImageFromWxBitmap( wxBmap ) )
#end def

#----------------------------

def WxBitmapFromPilImage( pilImage, wantAlpha=True, createAlpha=False, threshold=128 ) :   # 3 ==> 1
    return WxBitmapFromWxImage( WxImageFromPilImage( pilImage, wantAlpha, createAlpha ), threshold=128 )
#end def

def WxImageFromPilImage( pilImage, wantAlpha=True, createAlpha=False ) :    # 3 ==> 2
    """    
    If the given pilImage has alpha, then preserve it in the wxImage (the default)
      unless alpha preservation is specifically disabled by setting wantAlpha=False.
    
    If the given pilImage mode is RGB, optionally create a new wxImage alpha plane/band 
      by setting createAlpha=True.
    """
    if (pilImage.mode == 'RGBA') :       # ignore flag createAlpha since pilImage is already RGBA
        
        wxImage = wx.EmptyImage( *pilImage.size  )      # Also reads alpha if present.
        
        pilRgbImage = pilImage      # Do NOT let Pil's IN-PLACE conversion alter the original image !
        pilRgbDataStr = pilRgbImage.convert( 'RGB' ).tobytes()   # "IN-PLACE" method alters the source !!
        #pp(dir(pilRgbDataStr))
        #print(pilRgbDataStr)
        wxImage.SetData( pilRgbDataStr )    # Just the RGB data from the new RGB mode image.
        
        if wantAlpha :      # This is the default case.
            pilRgbaStr = pilImage.tobytes()    # Converts the RGBA planes into a list of data strings.
            # Extract just the existing alpha data from the the PilImage.
            pilAlphaStr = pilRgbaStr[3::4]      # start at index 3 with a stride (skip) of 4.
            # Copy the pilImage alpha string data into wxImage alpha plane.
            #pp(dir(wxImage))
            wxImage.SetAlpha( pilAlphaStr )
        #end if
        
    else :      # For all pilImages without an alpha plane/band/layer/channel.
        
        pilRgbImage = pilImage          # Copy to prevent Pil's in-place conversion altering the original image !
        if pilRgbImage.mode != 'RGB' :      # Convert non-RGB formats to RGB
            pilRgbImage = pilRgbImage.convert( 'RGB' )    # IN_PLACE_METHOD - alters the original image
        #end if
        
        #wxImage = wx.EmptyImage( pilRgbImage.size[0], pilRgbImage.size[1] )    # Alternate
        wxImage = wx.EmptyImage( *pilRgbImage.size )
        wxImage.SetData( pilRgbImage.tostring() )     
        
        # When createAlpha=True create a new wxImage alpha plane/channel/band/layer.
        if createAlpha :
            # Create and insert 100% opaque alpha (values=255) 
            # .convert( 'RGBA' ) always adds a brand new 100% opaque pilImage alpha plane.
            # .SetAlphaData() adds a brand new wxImage alpha plane in this case
            #   since the wxImage doesn't originally have any alpha plane.
            pilRgbaImage = pilRgbImage.convert( 'RGBA' )      # Create an alpha plane
            wxImage.SetAlphaData( pilRgbaImage.convert( 'RGBA' ).tostring()[3::4] )
        #end if
        
    #end if
    
    return wxImage      # May or may not have an alpha plane depending on 
                        #   the input image mode and the given option flags.
#end def

#----------------------------

def WxBitmapFromWxImage( wxImage, threshold=128 ) :    # 2 ==> 1
    
    working_wxImage = wxImage          # Don't change the original.
    working_wxImage.ConvertAlphaToMask( threshold=threshold )
    bmap = wxImage.ConvertToBitmap()
    
    return bmap
    
#end def

def PilImageFromWxImage( wxImage, wantAlpha=True ) :   # 2 ==> 3  Default is to keep any alpha channel
    
    image_size = wxImage.GetSize()      # All images here have the same size.
    
    # Create an RGB pilImage and stuff it with RGB data from the wxImage.
    pilImage = Image.new( 'RGB', image_size )
    pilImage.fromstring( wxImage.GetData() )
    
    if wantAlpha and wxImage.HasAlpha() :   # Only wx.Bitmaps use .ConvertAlphaToMask( [0..255] )

        # Create an L pilImage and stuff it with the alpha data extracted from the wxImage.
        l_pilImage = Image.new( 'L', image_size )
        l_pilImage.fromstring( wxImage.GetAlphaData() )

        # Create an RGBA pil image from the 4 bands.
        r_pilImage, g_pilImage, b_pilImage = pilImage.split()
        pilImage = Image.merge( 'RGBA', (r_pilImage, g_pilImage, b_pilImage, l_pilImage) )

    #end if
    
    return pilImage
    
#end def PilImageFromWxImage

#------------------------------------------------------------------------------