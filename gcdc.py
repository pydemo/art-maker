import wx
import random

class Panel(wx.Panel):
	def __init__(self, *args, **kwargs):
		kwargs['style'] = kwargs.setdefault('style', wx.NO_FULL_REPAINT_ON_RESIZE) | wx.NO_FULL_REPAINT_ON_RESIZE
		super().__init__( *args, **kwargs)	
		#super(Panel, self).__init__(parent, -1)
		#self.Bind(wx.EVT_PAINT, self.on_paint)
		self.done=False
		self.USE_BUFFERED_DC =True
		self.Bind(wx.EVT_PAINT,self.OnPaint)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		w,h=wx.GetApp().GetTopWindow().GetSize()
		cnt=10000
		if 0:
			xx1= [random.randint(int(w/3),int( w*2/3)) for j in range(cnt)]
			yy1 = [random.randint(0, h) for x in xx1]
			xx2= [random.randint(0, w) for j in range(cnt)]
			yy2 = [random.randint(h-x, h) if x<w/2 else random.randint(x-h/2, h) for x in xx2]
		blank = [w/2-50,h/2-50, w/2+50, h/2+50]
		yy1 = [random.randint(0, h) for j in range(cnt)]
		xx1 = [random.randint(int(w/2-y/2), int(w/2+y/2)) for y in yy1]
		yy2 = [random.randint(0, h) for j in range(cnt)]
		xx2 = [random.randint(int(w/2-y/2), int(w/2+y/2)) for y in yy2]		
		
		self.lines = [ x for x in [\
			[xx1[j], yy1[j],xx2[j], yy2[j]] \
		for j in range(cnt)] if True]
		
		#b = self.in_blank(self.lines[0], blank)
		#print(b)
		line1= [0, 10, 50,40]
		line2= [0, 50, 50,50]
		print(self.get_inter(*line1, *line2))
		self.lines =[line1, line2]
	@staticmethod
	def get_inter(x1,y1,x2,y2,x3,y3,x4,y4):
		px= ( (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) ) 
		py= ( (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) )
		return [px, py]		
	@staticmethod
	def not_in_blank(line, blank):
		top = blank[:2]
		bottom = blank[-2:]
		l1 = line[:2]
		l2 = line[-2:]
		#print(l1,l2)
		#print(top,bottom)
		return (not top<l1 and l1<bottom) 

	def draw_it(self, dc):
		dc.SetBackground( wx.Brush("White") )
		dc.Clear()
		#dc.SetUserScale(0.5,1)		
		if 0: #not self.done:
			if self.USE_BUFFERED_DC:
				self.dc1 = wx.BufferedPaintDC(self, self._Buffer)
			else:
				self.dc1 = wx.PaintDC(self)
			#dc = wx.PaintDC(self)
			self.dc = wx.GCDC(self.dc1)
			#
		self.dc = wx.GCDC(dc)
		for i, line in enumerate(self.lines):
			self.dc.DrawLine(*line)
			if i%1000 ==0:
				print(line, i%1000, i)
			self.done=True


	def UpdateDrawing(self):
		'''
		 This would get called if the drawing is changed, for whatever reason.

		 The idea here is that the drawing is based on some data generated
		 elsewhere in the system. If that data changes, the drawing needs to
		 be updated.

		 This code re-draws the buffer, then calls Update, which forces a paint event.
		'''
		dc = wx.MemoryDC()
		dc.SelectObject(self._Buffer)
		self.draw_it(dc)
		del dc      # need to get rid of the MemoryDC before Update() is called.
		self.Refresh()
		self.Update()
		
		
	def Draw(self, dc):
		'''
		 just here as a place holder.
		 This method must be over-ridden when subclassed
		'''
		pass

	def OnPaint(self, event):
		'''
		  All that is needed here is to move the buffer to the screen
		'''
		if self.USE_BUFFERED_DC:
			dc = wx.BufferedPaintDC(self, self._Buffer)
		else:
			dc = wx.PaintDC(self)
			dc.DrawBitmap(self._Buffer, 0, 0)

	def OnSize(self,event):
		'''
		 The Buffer init is done here, to make sure the buffer is always
		 the same size as the Window
		'''
		Size  = self.ClientSize

		# Make new offscreen bitmap: this bitmap will always have the
		# current drawing in it, so it can be used to save the image to
		# a file, or whatever.
		self._Buffer = wx.Bitmap(*Size)
		self.UpdateDrawing()
		
class Frame(wx.Frame):
	def __init__(self,*args, **kwargs):

		super(Frame, self).__init__(None, -1, 'Test')
		self.SetPosition((50,25))
		self.SetSize((1300,1300))
		Panel(self)
		

if __name__ == "__main__":
	app = wx.App()
	frame = Frame()
	frame.Show()
	app.MainLoop()