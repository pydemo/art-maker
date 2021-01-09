import ctypes
import cairo

from ctypes.util import find_library

cairo_dll = ctypes.CDLL(find_library("cairo"))

# Pycairo's API representation (from pycairo.h)
class Pycairo_CAPI(ctypes.Structure):
   _fields_ = [
      ('Context_Type', ctypes.py_object),
      ('Context_FromContext', ctypes.PYFUNCTYPE(ctypes.py_object,
                                                ctypes.c_void_p,
                                                ctypes.py_object,
                                                ctypes.py_object)),
      ('FontFace_Type', ctypes.py_object),
      ('FontFace_FromFontFace', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
      ('FontOptions_Type', ctypes.py_object),
      ('FontOptions_FromFontOptions', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
      ('Matrix_Type', ctypes.py_object),
      ('Matrix_FromMatrix', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
      ('Path_Type', ctypes.py_object),
      ('Path_FromPath', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
      ('Pattern_Type', ctypes.py_object),
      ('SolidPattern_Type', ctypes.py_object),
      ('SurfacePattern_Type', ctypes.py_object),
      ('Gradient_Type', ctypes.py_object),
      ('LinearGradient_Type', ctypes.py_object),
      ('RadialGradient_Type', ctypes.py_object),
      ('Pattern_FromPattern', ctypes.c_void_p),
      ('ScaledFont_Type', ctypes.py_object),
      ('ScaledFont_FromScaledFont', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
      ('Surface_Type', ctypes.py_object),
      ('ImageSurface_Type', ctypes.py_object),
      ('PDFSurface_Type', ctypes.py_object),
      ('PSSurface_Type', ctypes.py_object),
      ('SVGSurface_Type', ctypes.py_object),
      ('Win32Surface_Type', ctypes.py_object),
      ('XlibSurface_Type', ctypes.py_object),
      ('Surface_FromSurface', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
      ('Check_Status', ctypes.PYFUNCTYPE(ctypes.c_int, ctypes.c_int))]

# look up the API
ctypes.pythonapi.PyCObject_Import.restype = ctypes.POINTER(Pycairo_CAPI)
pycairo_api = ctypes.pythonapi.PyCObject_Import("cairo", "CAPI").contents;

ContextType = pycairo_api.Context_Type

def Context_FromSWIGObject(swigObj):
    ptr = ctypes.c_void_p(int(swigObj))
    #increment the native context's ref count, since the Pycairo_Context decrements it
    #when it is finalised.
    cairo_dll.cairo_reference(ptr)
    return pycairo_api.Context_FromContext(ptr, ContextType, None)

if __name__=="__main__":
    import wx
    import math

    class myframe(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, -1, "test", size=(500,400))
            self.Bind(wx.EVT_PAINT, self.OnPaint)

        def OnPaint(self, event):
            dc = wx.PaintDC(self)
            w,h = dc.GetSizeTuple()
            gc = wx.GraphicsContext.Create(dc)
            nc = gc.GetNativeContext()
            ctx = Context_FromSWIGObject(nc)

            #wxGC drawing calls
            gc.SetPen(wx.Pen("navy", 2))
            gc.SetBrush(wx.Brush("pink"))
            gc.DrawRectangle(w/4.,h/4.,w/2.,h/2.)

            #cairo drawing calls
            ctx.arc(2.*w/3,2.*h/3.,min(w,h)/4. - 10,0, math.pi*2)
            ctx.set_source_rgba(0,1,1,0.5)
            ctx.fill_preserve()
            ctx.set_source_rgb(1,0.5,0)
            ctx.stroke()

    app = wx.App()
    f = myframe()
    f.Show()
    app.MainLoop()