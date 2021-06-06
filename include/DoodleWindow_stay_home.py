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

		
def get_clrs(colours):
	prev=0
	while True:
		next = prev
		while next == prev:
			#print(prev, next)
			next = colours[randrange(0, len(colours))]
		yield next
from itertools import cycle
def get_letter(letters):

	pool = cycle([x for x in letters])

	return pool
		

		
step=10
def get_span(step):
	for i in range(100):
		yield step*(i+1)
class DoodleWindow(wx.Window):
	menuColours = { 99 : 'White',
					100 : 'Black',
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
		self.curLine = []


	def Cleanup(self, evt):
		if hasattr(self, "menu"):
			self.menu.Destroy()
			del self.menu

	def setBackground(dc):
		dc.SetBackground(wx.Brush(wx.RED))
		
	def InitBuffer(self):
		"""Initialize the bitmap used for buffering the display."""
		size = self.GetClientSize()
		self.buffer = wx.Bitmap(size.width, size.height)
		self.dc=dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		dc.SetBackground(wx.Brush(wx.WHITE))
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
		global colours
		"""Set a new colour and make a matching pen"""
		self.colour = colour
		self.pen = wx.Pen(self.colour, self.thickness, wx.SOLID)
		self.Notify()
		colours = next(nextclr)
		
		


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
			#dc = wx.GCDC(dc)
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
		#dc = wx.GCDC(dc)
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
		lsize=get_size(tlarge)
		ssize=get_size(tsmall)
		clr =get_color(colours)
		ltr= get_letter('S  t  a  y h   o  m   e  ')



		if 0:
			pen.SetWidth(next(size))
			pen.SetColour(wx.Colour(next(clr)))
			if 1:
				#pen.SetCap(caps[randrange(0, len(caps))])
				pen.SetCap(wx.CAP_ROUND) 
				pen.SetJoin(wx.JOIN_ROUND)
			dc.SetPen(pen)
		if 1:
			x, y, *_ = coords
			#dc.DrawRectangle(x, y, 20, 20)
			#dc.DrawLine(*coords)
			if 1: #set background
				#font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
				#font =wx.Font(60, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "")
				#dc.SetForegroundColour(wx.NamedColour("YELLOW"))
				l=next(pool)
				if 1:
					if l in ['F','N']:
						s=next(size)
					else:
						s=next(ssize)
				#s=next(size)
				font = wx.Font(s, wx.SWISS, wx.NORMAL, wx.BOLD, False)
				#font.MakeSmaller()
				gc = wx.GraphicsContext.Create(dc)
				gc.SetFont(font, next(clr))
				#w, labelHeight = dc.GetTextExtent('Wy')
				#bmp = images.Smiles.GetBitmap()
				#bmp.SetMask(None)
				#brush = wx.Brush(bmp)
				#brush = wx.Brush(wx.RED, wx.SOLID)
				#gc.SetBrush(brush)
				
				#print(l)
				gc.DrawText(l, x, y)
			



	# Observer pattern.  Listeners are registered and then notified
	# whenever doodle settings change.
	def AddListener(self, listener):
		self.listeners.append(listener)

	def Notify(self):
		for other in self.listeners:
			other.Update(self.colour, self.thickness)
	def setColours(self, clrs):
		global colours
		colours = clrs
if 1:
	from itertools import cycle

	lst = [x.upper() for x in 'F      r      e        N      a      v      a      l    n   y ']
	#lst = [x for x in 'S      t      a      y                        H      o      m      e ']
	#lst = 'STAY HOME'

	pool = cycle(lst)		
thicknesses = [6,  12, 24,12, 24,12, 24,12, 24,12, 24,12, 24, 48, 60]
tlarge = [180,  270 ,  390]
tsmall = [60, 90, 120, 180,210, 240] 
thicknesses = tsmall+tlarge

join =[wx.JOIN_BEVEL, wx.JOIN_ROUND, wx.JOIN_MITER]

caps=[wx.CAP_ROUND , wx.CAP_PROJECTING] #, wx.CAP_BUTT]
caps=[wx.CAP_ROUND]
clrs = []
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
clrs.append(colours)
if 0:
	colours =  ['#e7ebee','#6c7197','#739211','#080300','#d92405','#3563eb','#eac124'] #BIRD
	clrs.append(colours)
	colours =  ['#60bdaf', '#a1d8b1', '#edfcc2', '#f88aaf', '#455655'] #Michael Cina
	clrs.append(colours)
	colours = ['#d7dddb', '#4f8a83', '#e76278', '#fac699', '#712164'] #Baloons
	clrs.append(colours)
	colours = ['#585340', '#b7ae9d', '#fafffc', '#accecd', '#8a151b', '#bc6367'] #Ryde
	clrs.append(colours)
	colours = ['#51574a', '#447c69', '#74c493', '#8e8c6d', '#e4bf80', '#e9d78e', '#e2975d', '#f19670', '#e16552', '#c94a53', '#be5168', '#a34974',\
	'#993767', '#65387d', '#4e2472', '#9163b6', '#e279a3', '#e0598b', '#7c9fb0', '#5698c4', '#9abf88'] #trove
	clrs.append(colours)
	colours = ['#f7fcf0', '#e0f3db', '#ccebc5', '#a8ddb5', '#7bccc4', '#4eb3d3', '#2b8cbe', '#0868ac', '#084081'] #Toni
	clrs.append(colours)
	colours = ['#1a1334', '#26294a', '#01545a', '#017351', '#03c383', '#aad962', '#fbbf45', '#ef6a32', '#ed0345', '#a12a5e', '#710162', '#110141'] #Colores
	clrs.append(colours)
	colours = ['#fc6472', '#f4b2a6', '#eccdb3', '#bcefd0', '#a1e8e4', '#23c8b2', '#c3ecee'] #Pleasant
	clrs.append(colours)
	colours = ['#faa818', '#41a30d', '#ffce38', '#367d7d', '#d33502', '#6ebcbc', '#37526d'] #Van Gogh
	clrs.append(colours)
	colours = ['#c000a4', '#5c015e', '#5225d8', '#2a0161', '#0106d1', '#06004b'] #Royal
	clrs.append(colours)
	colours = ['#2060ff', '#209fff', '#20bfff', '#00cfff', '#2affff', '#55ffff', '#7fffff', '#aaffff', '#ffff54', '#fff000', '#ffbf00', '#ffa800',\
	'#ff8a00', '#ff7000', '#ff4d00', '#ff0000']
	clrs.append(colours)


	"""Almond (#EFE3CE), 
	Dutch White (#E4D7B9), 
	Ruddy Pink (#DE9297), 
	Pastel Pink (#DEA5A4), 
	Pale Chestnut (#DEB2A8) and Desert Sand (#E2C1B8).
	"""
	colours = ['#EFE3CE', '#E4D7B9', '#DE9297', '#DEA5A4', '#DEB2A8', '#E2C1B8','#ffd1dc', '#000000']
	clrs.append(colours)
	""" Brilliance Of Rose
	Dogwood Rose (#D71768), 
	Cerise Pink (#ED2F85), 
	Brilliant Rose (#FD56A6), 
	Deep Moss Green (#376E47) and 
	Dark Green (#082E04).
	"""
	colours = ['#D71768', '#ED2F85', '#FD56A6', '#376E47', '#082E04']
	clrs.append(colours)
	"""Authentic Unicorn Color Scheme
	Cosmic Cobalt (#3B3285),
	 Blue-Green (#08A4B1), 
	 Android Green (#A6CB3F), 
	 Citrine (#E7D614), 
	 Marigold (#EEAE21) and 
	 Dark Pink (#EF517F).
	 """
	colours = ['#3B3285', '#08A4B1', '#A6CB3F', '#E7D614', '#EEAE21', '#EF517F']
	clrs.append(colours)
	"""4th July Gold Card 
	CB2D2E
	 Green-Blue (#1463B8), 
	 Rich Electric Blue (#0696D3), 
	 Golden Yellow (#FFDF00), 
	 Deep Carmine Pink (#FFDF00) and 
	 Persian Red (#CB2D2E)."""
	colours = ['#1463B8', '#0696D3', '#FFDF00', '#FFDF00', '#CB2D2E']
	clrs.append(colours)
	""" Gold Coast Football Club Logo
	Vivid Yellow (#FFE010), 
	Crimson Glory (#B90A34), 
	Lust (#E92A1F), 
	Orange Soda (#F15D42), 
	Burnt Sienna (#F37755) and 
	Blue (NCS) (#0681C2)."""
	colours = ['#FFE010', '#B90A34', '#E92A1F', '#F15D42', '#F37755', '#0681C2']
	clrs.append(colours)
	"""Hawaiian Airlines Logo Colors with Hex & RGB Codes has 5 colors which are 
	Dark Slate Blue (#413691),
	Deep Carmine Pink (#EF3138), 
	Blue-Magenta Violet (#523090), 
	Dark Magenta (#9D178D) and 
	Medium Violet-Red (#D2058A).
	"""
	colours = ['#413691', '#EF3138', '#523090', '#9D178D', '#D2058A']
	clrs.append(colours)

	"""
	 British Airways Website Colors with Hex & RGB Codes has 6 colors which are 
	Medium Persian Blue (#075AAA), 
	Red (Pigment) (#EB2226), 
	Cool Black (#01295C), 
	Beau Blue (#B9CFED), 
	Alabaster (#EFE9E5) and 
	Metallic Silver (#A7A9AC).
	"""
	colours = ['#075AAA', '#EB2226', '#01295C', '#B9CFED', '#EFE9E5', '#A7A9AC']
	clrs.append(colours) 
	"""
	  I Like It Color Scheme palette has 6 colors which are 
	  Cyclamen (#F96DAA), Light Hot Pink (#FFBAE7), 
	  Lemon Glacier (#FEFF00), 
	  Vivid Sky Blue (#02D0FF), 
	  Golden Poppy (#F9C307) and 
	  Silver Lake Blue (#5A82BE).
	"""
	colours = ['#F96DAA', '#FFBAE7', '#FEFF00', '#02D0FF', '#F9C307', '#5A82BE']
	clrs.append(colours)
	"""
	 Alexa Website Colors with Hex & RGB Codes has 4 colors which are 
	 Japanese Indigo (#233D53), 
	 Dark Cerulean (#064B73), 
	 Linen (#F9F3E6) and 
	 Portland Orange (#FA532E).
	"""
	colours = ['#233D53', '#064B73', '#F9F3E6', '#FA532E']
	clrs.append(colours)
	"""
	 Apple Rainbow Logo Colors with Hex & RGB Codes has 6 colors which are 
	 Apple (#5EBD3E), 
	 Selective Yellow (#FFB900), 
	 University Of Tennessee Orange (#F78200),
	 CG Red (#E23838), 
	 Cadmium Violet (#973999) and 
	 Rich Electric Blue (#009CDF).
	"""
	colours = ['#5EBD3E', '#FFB900', '#F78200', '#E23838','#973999', '#009CDF' ]
	clrs.append(colours)
	""" Peacock
	 362315	11F3FF	0CB9F3	016BD1	FDF958	535313
	"""
	colours = ['#362315', '#11F3FF', '#0CB9F3', '#016BD1','#FDF958', '#535313' ]
	clrs.append(colours)
	"""
	  Mozilla Firefox Logo 2017 Colors with Hex & RGB Codes has 6 colors which are 
	  Medium Violet-Red (#BE0575),
	  Imperial Red (#F62336), 
	  Orange-Red (#FF6611), 
	  Lemon Yellow (#FFEC4A), 
	  Denim Blue (#203FB6) and 
	  Azure (#008AFB).
	"""
	colours = ['#BE0575', '#F62336', '#FF6611', '#FFEC4A','#203FB6', '#008AFB' ]

	clrs.append(colours)

nextclr = get_clrs(clrs)