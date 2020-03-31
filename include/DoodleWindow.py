import wx                  # This module uses the new wx namespace
from random import randrange
from pprint import pprint as pp
#----------------------------------------------------------------------



def get_color(colours):
	prev=''
	while True:
		next = prev
		while next == prev:
			#print(prev, next)
			next = colours[randrange(0, len(colours))]
		yield next
def get_size(thicknesses):
	prev=0
	while True:
		next = prev
		while next == prev:
			#print(prev, next)
			next = thicknesses[randrange(0, len(thicknesses))]
		yield next
		
def get_cap(caps):
	prev=0
	while True:
		next = prev
		while next == prev:
			#print(prev, next)
			next = caps[randrange(0, len(caps))]
		yield next
		
step=10
def get_span(step):
	for i in range(100):
		yield step*(i+1)
class DoodleWindow(wx.Window):
	menuColours = { 100 : 'Black',
					101 : 'Yellow',
					102 : 'Red',
					103 : 'Green',
					104 : 'Blue',
					105 : 'Purple',
					106 : 'Brown',
					107 : 'Aquamarine',
					108 : 'Forest Green',
					109 : 'Light Blue',
					110 : 'Goldenrod',
					111 : 'Cyan',
					112 : 'Orange',
					113 : 'Navy',
					114 : 'Dark Grey',
					115 : 'Light Grey',
					}
	maxThickness = 16


	def __init__(self, parent, ID):
		wx.Window.__init__(self, parent, ID, style=wx.NO_FULL_REPAINT_ON_RESIZE)
		self.SetBackgroundColour("WHITE")
		self.listeners = []
		self.thickness = 1
		self.SetColour("Black")
		self.lines = []
		self.pos = wx.Point(0,0)
		#self.MakeMenu()

		self.InitBuffer()

		self.SetCursor(wx.Cursor(wx.CURSOR_PENCIL))

		# hook some mouse events
		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
		self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
		self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
		self.Bind(wx.EVT_MOTION, self.OnMotion)

		# the window resize event and idle events for managing the buffer
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_IDLE, self.OnIdle)

		# and the refresh event
		self.Bind(wx.EVT_PAINT, self.OnPaint)

		# When the window is destroyed, clean up resources.
		self.Bind(wx.EVT_WINDOW_DESTROY, self.Cleanup)


	def Cleanup(self, evt):
		if hasattr(self, "menu"):
			self.menu.Destroy()
			del self.menu


	def InitBuffer(self):
		"""Initialize the bitmap used for buffering the display."""
		size = self.GetClientSize()
		self.buffer = wx.Bitmap(size.width, size.height)
		self.dc=dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
		dc.Clear()
		width, height = self.GetClientSize()
		if 0: #set background
			font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
			font.MakeSmaller()
			dc.SetFont(font)
			w, labelHeight = dc.GetTextExtent('Wy')
			#bmp = images.Smiles.GetBitmap()
			#bmp.SetMask(None)
			#brush = wx.Brush(bmp)
			brush = wx.Brush(wx.BLACK, wx.SOLID)
			#dc.DrawText('test', 1, 1)

			dc.SetBrush(brush)
			dc.DrawRectangle(5, labelHeight+2, width-10, height-labelHeight-5-2)
		#dc = wx.GCDC(dc)
		
		self.DrawLines(dc)
		self.reInitBuffer = False


	def SetColour(self, colour):
		"""Set a new colour and make a matching pen"""
		self.colour = colour
		self.pen = wx.Pen(self.colour, self.thickness, wx.SOLID)
		self.Notify()


	def SetThickness(self, num):
		"""Set a new line thickness and make a matching pen"""
		self.thickness = num
		self.pen = wx.Pen(self.colour, self.thickness, wx.SOLID)
		self.Notify()


	def GetLinesData(self):
		return self.lines[:]


	def SetLinesData(self, lines):
		self.lines = lines[:]
		self.InitBuffer()
		self.Refresh()



	def OnLeftDown(self, event):
		"""called when the left mouse button is pressed"""
		self.curLine = []
		self.pos = event.GetPosition()
		self.CaptureMouse()


	def OnLeftUp(self, event):
		"""called when the left mouse button is released"""
		if self.HasCapture():
			self.lines.append( (self.colour, self.thickness, self.curLine) )
			self.curLine = []
			self.ReleaseMouse()


	def OnRightUp(self, event):
		"""called when the right mouse button is released, will popup the menu"""
		pt = event.GetPosition()
		self.PopupMenu(self.menu, pt)



	def OnMotion(self, event):
		"""
		Called when the mouse is in motion.  If the left button is
		dragging then draw a line from the last event position to the
		current one.  Save the coordinants for redraws.
		"""
		if event.Dragging() and event.LeftIsDown():
			dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
			
			#dc.SetPen(self.pen)
			pos = event.GetPosition()
			coords = (self.pos.x, self.pos.y, pos.x, pos.y)
			self.curLine.append(coords)
			if 1:
				pen = wx.Pen(self.colour, self.thickness, wx.SOLID)
				#pp(dir(pen))
				dc.SetPen(pen)
			dc = wx.GCDC(dc)
			self.drawCoords(dc, coords, pen)
			self.pos = pos
			


	def OnSize(self, event):
		"""
		Called when the window is resized.  We set a flag so the idle
		handler will resize the buffer.
		"""
		self.reInitBuffer = True


	def OnIdle(self, event):
		"""
		If the size was changed then resize the bitmap used for double
		buffering to match the window size.  We do it in Idle time so
		there is only one refresh after resizing is done, not lots while
		it is happening.
		"""
		if self.reInitBuffer:
			self.InitBuffer()
			self.Refresh(False)


	def OnPaint(self, event):
		"""
		Called when the window is exposed.
		"""
		# Create a buffered paint DC.  It will create the real
		# wx.PaintDC and then blit the bitmap to it when dc is
		# deleted.  Since we don't need to draw anything else
		# here that's all there is to it.
		dc = wx.BufferedPaintDC(self, self.buffer)


	def DrawLines(self, dc):
		"""
		Redraws all the lines that have been drawn already.
		"""
		dc = wx.GCDC(dc)
		for colour, thickness, line in self.lines:
			pen = wx.Pen(colour, thickness, wx.SOLID)
			#pp(dir(pen))
			dc.SetPen(pen)
			#print(len(line))
			
			for coords in line:
				self.drawCoords(dc, coords, pen)
	@staticmethod
	def drawCoords(dc, coords, pen):
		

		brush= wx.SHORT_DASH		
		size=get_size(thicknesses)
		clr =get_color(colours)
		if 1:

			pen.SetWidth(next(size))
			pen.SetColour(wx.Colour(next(clr)))
			if 1:
				#pen.SetCap(caps[randrange(0, len(caps))])
				pen.SetCap(wx.CAP_ROUND) 
			#
			if 1:
				pen.SetJoin(wx.JOIN_ROUND)
				
				
			dc.SetPen(pen)
		
		if 1:
			x, y, *_ = coords
			dc.DrawRectangle(x, y, 20, 20)
			dc.DrawLine(*coords)



	# Observer pattern.  Listeners are registered and then notified
	# whenever doodle settings change.
	def AddListener(self, listener):
		self.listeners.append(listener)

	def Notify(self):
		for other in self.listeners:
			other.Update(self.colour, self.thickness)

thicknesses = [6,  12, 24,12, 24,12, 24,12, 24,12, 24,12, 24, 48, 60]
join =[wx.JOIN_BEVEL, wx.JOIN_ROUND, wx.JOIN_MITER]

caps=[wx.CAP_ROUND , wx.CAP_PROJECTING] #, wx.CAP_BUTT]
caps=[wx.CAP_ROUND]
		
colours =  ['#e7ebee','#6c7197','#739211','#080300','#d92405','#3563eb','#eac124'] #BIRD
#colours =  colours+['#60bdaf', '#a1d8b1', '#edfcc2', '#f88aaf', '#455655'] #Michael Cina
colours =  colours+['#d7dddb', '#4f8a83', '#e76278', '#fac699', '#712164'] #Baloons
colours = colours+ ['#585340', '#b7ae9d', '#fafffc', '#accecd', '#8a151b', '#bc6367'] #Ryde
#colours = colours+['#51574a', '#447c69', '#74c493', '#8e8c6d', '#e4bf80', '#e9d78e', '#e2975d', '#f19670', '#e16552', '#c94a53', '#be5168', '#a34974',\
#'#993767', '#65387d', '#4e2472', '#9163b6', '#e279a3', '#e0598b', '#7c9fb0', '#5698c4', '#9abf88'] #trove
colours = colours+['#f7fcf0', '#e0f3db', '#ccebc5', '#a8ddb5', '#7bccc4', '#4eb3d3', '#2b8cbe', '#0868ac', '#084081'] #Toni
colours = colours+['#1a1334', '#26294a', '#01545a', '#017351', '#03c383', '#aad962', '#fbbf45', '#ef6a32', '#ed0345', '#a12a5e', '#710162', '#110141'] #Colores
colours = colours+['#fc6472', '#f4b2a6', '#eccdb3', '#bcefd0', '#a1e8e4', '#23c8b2', '#c3ecee'] #Pleasant
colours = colours+['#faa818', '#41a30d', '#ffce38', '#367d7d', '#d33502', '#6ebcbc', '#37526d'] #Van Gogh
colours = colours+['#c000a4', '#5c015e', '#5225d8', '#2a0161', '#0106d1', '#06004b'] #Royal
colours = colours+['#2060ff', '#209fff', '#20bfff', '#00cfff', '#2affff', '#55ffff', '#7fffff', '#aaffff', '#ffff54', '#fff000', '#ffbf00', '#ffa800',\
'#ff8a00', '#ff7000', '#ff4d00', '#ff0000']