# doodle.py

'''
This module contains the DoodleWindow class which is a window that you
can do simple drawings upon.
'''

import wx
from random import randrange
from pprint import pprint as pp

if 1:
	colours = ['Black', 'Yellow', 'Red', 'Green', 'Blue', 'Purple', 
		'Brown', 'Aquamarine', 'Forest Green', 'Light Blue', 'Goldenrod', 
		'Cyan', 'Orange', 'Navy', 'Dark Grey', 'Light Grey']
	colours = ['#e7ebee','#6c7197','#739211','#080300','#d92405','#3563eb','#eac124'] #BIRD
	#colours = ['#60bdaf', '#a1d8b1', '#edfcc2', '#f88aaf', '#455655'] #Michael Cina
	#colours = ['#d7dddb', '#4f8a83', '#e76278', '#fac699', '#712164'] #Baloons
	colours = ['#585340', '#b7ae9d', '#fafffc', '#accecd', '#8a151b', '#bc6367'] #Ryde
	colours = ['#51574a', '#447c69', '#74c493', '#8e8c6d', '#e4bf80', '#e9d78e', '#e2975d', '#f19670', '#e16552', '#c94a53', '#be5168', '#a34974',\
'#993767', '#65387d', '#4e2472', '#9163b6', '#e279a3', '#e0598b', '#7c9fb0', '#5698c4', '#9abf88'] #trove
	colours = ['#f7fcf0', '#e0f3db', '#ccebc5', '#a8ddb5', '#7bccc4', '#4eb3d3', '#2b8cbe', '#0868ac', '#084081'] #Toni
	colours = ['#1a1334', '#26294a', '#01545a', '#017351', '#03c383', '#aad962', '#fbbf45', '#ef6a32', '#ed0345', '#a12a5e', '#710162', '#110141'] #Colores
	colours = ['#fc6472', '#f4b2a6', '#eccdb3', '#bcefd0', '#a1e8e4', '#23c8b2', '#c3ecee'] #Pleasant
	colours = ['#faa818', '#41a30d', '#ffce38', '#367d7d', '#d33502', '#6ebcbc', '#37526d'] #Van Gogh
	colours = ['#c000a4', '#5c015e', '#5225d8', '#2a0161', '#0106d1', '#06004b'] #Royal
	colours = ['#2060ff', '#209fff', '#20bfff', '#00cfff', '#2affff', '#55ffff', '#7fffff', '#aaffff', '#ffff54', '#fff000', '#ffbf00', '#ffa800',\
'#ff8a00', '#ff7000', '#ff4d00', '#ff0000']
	colours = ['#f4e1f0', '#f98a6b', '#d31b36', '#123e49', '#71999b', '#f9f7fc', '#fed760', '#fc648d', '#621a32', '#778cdf'] #drip
	colours = ['#c89e12', '#fdc100', '#ff8c00', '#fc3c07', '#b81313', '#6b2e13', '#472c00'] #fruit
	colours = ['#ea573d', '#fbc063', '#64b0bc', '#446699', '#555577'] #blue lagoon
	colours = colours+['#551177', '#ddaaff', '#ffccff', '#eeddff', '#ff0077'] #purple sunset
	#colours = colours+['#f6300a', '#d11b7e', '#f6ef2a', '#00c000', '#0a62da'] #installation
	#colours = ['#7f0000', '#cc0000', '#ff4444', '#ff7f7f', '#ffb2b2', '#995100', '#cc6c00', '#ff8800', '#ffbb33', '#ffe564', '#2c4c00', '#436500'\
	#'#669900', '#99cc00', '#d2fe4c', '#3c1451', '#6b238e', '#9933cc', '#aa66cc', '#bc93d1', '#004c66', '#007299', '#0099cc', '#33b5e5',
	#'#8ed5f0', '#660033', '#b20058', '#e50072', '#ff3298', '#ff7fbf'] #Android
	#colours = colours+['#93b4c7', '#acf0b0', '#a499ca', '#f0fabc', '#bff7f4'] #kick and boo/ pastel
	# colours = colours+['#2962ae', '#d81835', '#fb2d18', '#ff41a8', '#6cf4ba'] #india
	#colours = colours+['#ec2b22', '#f05320', '#f68e1d', '#2284ed', '#001e2d'] #orange and blue
	#colours = colours+['#3e6db6', '#ee1133', '#3ec0aa', '#ffc600', '#222299'] #cores
	#colours = colours+['#f15450', '#a98606', '#644379', '#8a3764', '#c97863', '#7ec1d4', '#fbb014'] #Buddist energy
	#colours = colours+['#a200ff', '#e705ff', '#ffc600', '#ddff00', '#00ffa2', '#00ddff'] #sd mp1
	#colours = colours+['#00aaee', '#ff5500', '#910091', '#ff0099', '#ff8a00', '#88cc00', '#0077bb'] #blend insider
	#colours = colours+['#3a3a3a', '#808080', '#a8a8a8', '#d0d0d0', '#eeeeee', '#005f87', '#00afff', '#5fdf5f', '#87afdf', '#afafdf', '#afdf87', '#df8787','#dfaf87', '#dfafdf', '#ffffaf'] #x
	#colours = colours+['#ec3c8e', '#63bb1e', '#fded00', '#651daf'] #marijuana
	#colours = colours+['#ff0000', '#007c78', '#c4ff00', '#56061a', '#d646c6', '#ff3a9c', '#ffee68', '#ed2b00', '#ff4c4f', '#2cd7ff'] #underwater
	#colours = colours+['#faca07', '#06274c', '#0a529e', '#d3d0cb', '#274156']
	#colours = colours+ ['#6699cc', '#fff275', '#ff8c42', '#ff3c38', '#a23e48']
	#colours = colours+ ['#ffbe0b', '#fb5607', '#ff006e', '#8338ec', '#3a86ff'] #rainbow brights good1
	#colours = colours+['#0c120c', '#c20114', '#6d7275', '#c7d6d5', '#ecebf3'] # use me			good1
	#colours = colours+['#02010a', '#04052e', '#140152', '#22007c', '#0d00a4'] #
	#colours = colours+['#F0676E', '#5C51A6', '#3F61A6', '#54C3C2'] #Blue
	#colours = colours+['#F27405', '#F24405', '#F20505', '#8C0303'] #Red
	#colours = colours+['#F20544', '#044BD9', '#83A603', '#F2CB05']
	#colours = colours+['#D96A93', '#F5BD60', '#C2D2F2', '#F1B9CD']


class DoodleMenus(object):


	def __init__(self, parent):
		self.colours=colours
		self.thicknesses=thicknesses
		self.makeMenu()
		self.bindEvents()
		
	def makeMenu(self):
		''' Make a menu that can be popped up later. '''
		self.menu = wx.Menu()
		self.idToColourMap = self.addCheckableMenuItems(self.menu, 
			self.colours)
		self.bindMenuEvents(menuHandler=self.onMenuSetColour,
			updateUIHandler=self.onCheckMenuColours,
			ids=self.idToColourMap.keys())
		self.menu.Break() # Next menu items go in a new column of the menu
		if 1:
			self.idToThicknessMap = self.addCheckableMenuItems(self.menu,
				self.thicknesses, start=len(self.idToColourMap))
			self.bindMenuEvents(menuHandler=self.onMenuSetThickness,
				updateUIHandler=self.onCheckMenuThickness,
				ids=self.idToThicknessMap.keys())

	@staticmethod
	def addCheckableMenuItems(menu, items, start=0):
		''' Add a checkable menu entry to menu for each item in items. This
			method returns a dictionary that maps the menuIds to the
			items. '''
		idToItemMapping = {}
		for id, item in enumerate(items):
			menuId = id +start
			idToItemMapping[menuId] = item
			menu.Append(menuId, str(item), kind=wx.ITEM_CHECK)
		#pp(idToItemMapping)
		return idToItemMapping

	def bindMenuEvents(self, menuHandler, updateUIHandler, ids): 
		''' Bind the menu id's in the list ids to menuHandler and
			updateUIHandler. ''' 
		sortedIds = sorted(ids)
		firstId, lastId = sortedIds[0], sortedIds[-1]
		for event, handler in \
				[(wx.EVT_MENU_RANGE, menuHandler),
				 (wx.EVT_UPDATE_UI_RANGE, updateUIHandler)]:
			self.Bind(event, handler, id=firstId, id2=lastId)
	def bindEvents(self):
		for event, handler in [ \
				(wx.EVT_LEFT_DOWN, self.onLeftDown), # Start drawing
				(wx.EVT_LEFT_UP, self.onLeftUp),     # Stop drawing 
				(wx.EVT_MOTION, self.onMotion),      # Draw
				(wx.EVT_RIGHT_UP, self.onRightUp),   # Popup menu
				(wx.EVT_SIZE, self.onSize),          # Prepare for redraw
				(wx.EVT_IDLE, self.onIdle),          # Redraw
				(wx.EVT_PAINT, self.onPaint),        # Refresh
				(wx.EVT_WINDOW_DESTROY, self.cleanup)]:
			self.Bind(event, handler)
	# These two event handlers are called before the menu is displayed
	# to determine which items should be checked.
	def onCheckMenuColours(self, event):
		colour = self.idToColourMap[event.GetId()]
		event.Check(colour == self.currentColour)

	def onCheckMenuThickness(self, event):
		thickness = self.idToThicknessMap[event.GetId()]
		event.Check(thickness == self.currentThickness)

	# Event handlers for the popup menu, uses the event ID to determine
	# the colour or the thickness to set.
	def onMenuSetColour(self, event):
		self.currentColour = self.idToColourMap[event.GetId()]

	def onMenuSetThickness(self, event):
		self.currentThickness = self.idToThicknessMap[event.GetId()]

	def onRightUp(self, event):
		''' Called when the right mouse button is released, will popup
			the menu. '''
		self.PopupMenu(self.menu)

from itertools import cycle

lst = [ 0,1, 2, 3, 4]

pool = cycle(lst)


slst = [1024, 512, 256, 256,512,1024]

spool = cycle(slst)

rthik = [256, 256,512, 1024, 1536]
global_width = 32
penwidth =4

#--------------------
def targetBitmap_point(color, width=global_width):
	actual_width = int(width/8)+1
	bitmap = wx.Bitmap(actual_width, actual_width)
	dc = wx.MemoryDC()
	dc.SelectObject(bitmap)
	#dc.BeginDrawing()
	dc.Clear()
	dc.SetBrush(wx.Brush(color, wx.TRANSPARENT))
	dc.SetPen(wx.Pen(color, 1))
	for i in range(actual_width):
		for j in range(actual_width):
			dc.DrawPoint(i,j)
	#dc.EndDrawing()
	dc.SelectObject(wx.NullBitmap)
	bitmap.SetMask(wx.Mask(bitmap, wx.WHITE))
	return bitmap
	
	
#--------------------
def targetBitmap_plus(color, width=global_width):
	bitmap = wx.Bitmap(width, width)
	dc = wx.MemoryDC()
	dc.SelectObject(bitmap)
	#dc.BeginDrawing()
	dc.Clear()
	dc.SetBrush(wx.Brush(color, wx.TRANSPARENT))
	dc.SetPen(wx.Pen(color, penwidth))
	dc.DrawLine(width/2, 0, width/2, width)
	dc.DrawLine(0, width/2, width, width/2)
	#dc.EndDrawing()
	dc.SelectObject(wx.NullBitmap)
	bitmap.SetMask(wx.Mask(bitmap, wx.WHITE))
	return bitmap
#--------------------
def targetBitmap_square( color, width=global_width):
	bitmap = wx.Bitmap(width, width)
	dc = wx.MemoryDC()
	dc.SelectObject(bitmap)
	#dc.BeginDrawing()
	dc.Clear()
	dc.SetBrush(wx.Brush(color, wx.TRANSPARENT))
	dc.SetPen(wx.Pen(color, penwidth))
	dc.DrawRectangle(1, 1, width-2, width-2)
	#dc.DrawLine(1, 1, width-2, 1)
	#dc.DrawLine(1, 1, 1, width-2)
	#dc.DrawLine(1, width-2, width-2, width-1)
	#dc.DrawLine(width-2, 1, width-2, width-1)
	#dc.EndDrawing()
	dc.SelectObject(wx.NullBitmap)
	#bitmap.SetMask(wx.Mask(bitmap, wx.YELLOW))
	return bitmap

#--------------------
def targetBitmap_cross(color, width=global_width):
	bitmap = wx.Bitmap(width, width)
	dc = wx.MemoryDC()
	dc.SelectObject(bitmap)
	#dc.BeginDrawing()
	dc.Clear()
	dc.SetBrush(wx.Brush(color, wx.TRANSPARENT))
	dc.SetPen(wx.Pen(color, penwidth))
	dc.DrawLine(0, 0, width, width)
	dc.DrawLine(0, width, width, 0)
	#dc.EndDrawing()
	dc.SelectObject(wx.NullBitmap)
	bitmap.SetMask(wx.Mask(bitmap, wx.WHITE))
	return bitmap
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



class DoodleWindow(wx.Window,DoodleMenus):


	def __init__(self, parent):
		super(DoodleWindow, self).__init__(parent, size=wx.GetDisplaySize(),
			style=wx.NO_FULL_REPAINT_ON_RESIZE|wx.FULLSCREEN_NOSTATUSBAR)
		DoodleMenus.__init__(self, parent)
		self.initDrawing()
		self.colours = colours
		self.initBuffer()
		#self.FullScreen()
		#GetScreenSize
		#self.ShowFullScreen(not self.IsFullScreen())
		#self.SetSize(wx.GetDisplaySize())
		#self.Resize()

	def initDrawing(self):
		self.SetBackgroundColour('WHITE')
		self.currentThickness = self.thicknesses[-1] 
		self.currentColour = self.colours[0]
		self.lines = []
		self.previousPosition = (0, 0)



	def initBuffer(self):
		''' Initialize the bitmap used for buffering the display. '''
		size = self.GetClientSize()
		self.buffer = wx.Bitmap(size.width, size.height)
		self.dc=dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
		dc.Clear()
		width, height = self.GetClientSize()
		import images2 as images		
		if 1: #set background
			font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
			font.MakeSmaller()
			dc.SetFont(font)
			w, labelHeight = dc.GetTextExtent('Wy')
			bmp = images.Smiles.GetBitmap()
			bmp.SetMask(None)
			brush = wx.Brush(bmp)
			brush = wx.Brush(wx.BLACK, wx.SOLID)
			#dc.DrawText('test', 1, 1)

			dc.SetBrush(brush)
			dc.DrawRectangle(5, labelHeight+2, width-10, height-labelHeight-5-2)
			
		self.drawLines(dc, *self.lines)
		self.reInitBuffer = False


	# Event handlers:

	def onLeftDown(self, event):
		''' Called when the left mouse button is pressed. '''
		self.currentLine = []
		self.previousPosition = tuple(event.GetPosition())
		self.CaptureMouse()

	def onLeftUp(self, event):
		''' Called when the left mouse button is released. '''
		if self.HasCapture():
			self.lines.append((self.currentColour, self.currentThickness, 
				self.currentLine))
			self.currentLine = []
			self.ReleaseMouse()

	def onMotion(self, event):
		''' Called when the mouse is in motion. If the left button is
			dragging then draw a line from the last event position to the
			current one. Save the coordinants for redraws. '''

		if event.Dragging() and event.LeftIsDown():
			dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)


		
			#dc=self.dc
			#pp(dir(event))
			currentPosition = tuple(event.GetPosition())
			lineSegment = self.previousPosition + currentPosition
			#print(lineSegment)
			#pool
			self.drawLines(dc, (next(get_color(self.colours)), next(get_size(self.thicknesses)) , 
				[lineSegment]))
			self.currentLine.append(lineSegment)
			self.previousPosition = currentPosition

	def onSize(self, event):
		''' Called when the window is resized. We set a flag so the idle
			handler will resize the buffer. '''
		self.reInitBuffer = True

	def onIdle(self, event):
		''' If the size was changed then resize the bitmap used for double
			buffering to match the window size.  We do it in Idle time so
			there is only one refresh after resizing is done, not lots while
			it is happening. '''
		if self.reInitBuffer:
			self.initBuffer()
			self.Refresh(False)

	def onPaint(self, event):
		''' Called when the window is exposed. '''
		# Create a buffered paint DC.  It will create the real
		# wx.PaintDC and then blit the bitmap to it when dc is
		# deleted.  Since we don't need to draw anything else
		# here that's all there is to it.
		dc = wx.BufferedPaintDC(self, self.buffer)
		#print(1)

	def cleanup(self, event):
		if hasattr(self, "menu"):
			self.menu.Destroy()
			del self.menu

	# Other methods
	@staticmethod
	def drawLines(dc, *lines):
		''' drawLines takes a device context (dc) and a list of lines
		as arguments. Each line is a three-tuple: (colour, thickness,
		linesegments). linesegments is a list of coordinates: (x1, y1,
		x2, y2). '''
		"""
		Style Description
		wx.BDIAGONAL_HATCH The pen will draw backward (northwest to southeast) hatch lines.
		wx.CROSSDIAG_HATCH A combination of wx.bdiagonal_hatch and wx.fdiagonal_hatch— in other words, it creates x shapes.
		wx.CROSS_HATCH Crosshatched + shapes.
		wx.DOT Small dots.
		wx.DOT_DASH Alternating between small dots and longer dashes.
		wx.FDIAGONAL_HATCH The pen will draw forward (southwest to northeast) hatch lines.
		wx.HORIZONTAL_HATCH Short, horizontal hash lines.
		wx.LONG_DASH Long dashes.
		"""		
		pen_styles = ["wx.SOLID", "wx.TRANSPARENT", "wx.DOT", "wx.LONG_DASH",
					  "wx.SHORT_DASH", "wx.DOT_DASH", "wx.BDIAGONAL_HATCH",
					  "wx.CROSSDIAG_HATCH", "wx.FDIAGONAL_HATCH", "wx.CROSS_HATCH",
					  "wx.HORIZONTAL_HATCH", "wx.VERTICAL_HATCH", "wx.USER_DASH"]
		if 'wxMSW' in wx.PlatformInfo:
			pen_styles.append("wx.STIPPLE")

		brush_styles = ["wx.SOLID", "wx.TRANSPARENT", "wx.STIPPLE", "wx.BDIAGONAL_HATCH",
						"wx.CROSSDIAG_HATCH", "wx.FDIAGONAL_HATCH", "wx.CROSS_HATCH",
						"wx.HORIZONTAL_HATCH", "wx.VERTICAL_HATCH"]
		
		#dc.BeginDrawing()
		if 0:
			ctx = wx.GraphicsContext.Create(dc)
			pen = ctx.CreatePen(wx.GraphicsPenInfo(wx.BLUE).Width(1.25).Style(wx.PENSTYLE_DOT))
			ctx.SetPen(pen)
		#colours = ['#e7ebee','#6c7197','#739211','#080300','#d92405','#3563eb','#eac124']
		if 0:
			import images2
			#stippleBitmap = images2.Smiles.GetBitmap()
			stippleBitmap = targetBitmap_point(wx.RED)
		
		#wx.SOLID+wx.CAP_PROJECTING
		cap = wx.CAP_BUTT
		caps=[wx.CAP_ROUND , wx.CAP_PROJECTING] #, wx.CAP_BUTT]
		caps=[wx.CAP_BUTT]
		brush= wx.DOT
		for colour, thickness, lineSegments in lines:
			pen = wx.Pen(wx.Colour(colour), thickness, brush)
			if 0: #Fill-in
				pen.SetStipple(stippleBitmap)
			#CAP_ROUND , CAP_PROJECTING and CAP_BUTT
			if 1:
				#print(next(capsp))
				#pen.SetCap(caps[randrange(0, len(caps))])
				pen.SetCap(next(get_cap(caps)))
			#JOIN_BEVEL , JOIN_ROUND and JOIN_MITER 
			if 0:
				pen.SetJoin(wx.JOIN_MITER)
			#pen.SetDashes([2, 5, 2, 2])
			#bitmap.SetMask(wx.Mask(bitmap, wx.WHITE)) #  It will allow you to mark places that should be transparent
			#dc.SetBrush(wx.Brush(wx.Colour(colours[randrange(0, len(colours))]), wx.TRANSPARENT))
			
			dc.SetPen(pen)
			if len(lineSegments)>1:
				pass
				if 0:
					pp(lineSegments)
					for lineSegment in lineSegments:
						pp(lineSegment)
						dc.DrawLine(*lineSegments[0])
			elif len(lineSegments)>0:
				line=lineSegments[0]
				dc.DrawLine(*line)
				span=25
				tk= get_size(thicknesses) #[thickness]) #thicknesses)
				colr = get_color(colours)
				cap=get_cap(caps)
				if 1:
					pen = wx.Pen(wx.Colour(next(colr)), next(tk), brush) 
					pen.SetCap(next(cap))
					dc.SetPen(pen)
				dc.DrawLine(*[x+span*1 for x in line])
				if 1:
					pen = wx.Pen(wx.Colour(next(colr)), next(tk), brush) 
					pen.SetCap(next(cap))
					dc.SetPen(pen)				
				dc.DrawLine(*[x+span*2 for x in line])
				if 1:
					pen = wx.Pen(wx.Colour(next(colr)), next(tk),brush) 
					pen.SetCap(next(cap))
					dc.SetPen(pen)				
				dc.DrawLine(*[x+span*3 for x in line])
				if 1:
					pen = wx.Pen(wx.Colour(next(colr)), next(tk), brush) 
					pen.SetCap(next(cap))
					dc.SetPen(pen)				
				dc.DrawLine(*[x+span*4 for x in line])
				
		#dc.EndDrawing()
thicknesses = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 256, 512]
thicknesses = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128,  1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 1, 2, 3, 4, 6,8, 12, 16, 24, 32, 48, 64,  1, 2, 3, 4, 6,8, 12, 16, 24, 32, 48,]
thicknesses = [  1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48,  1, 2, 3, 4, 6,8, 12, 16, 24, 32,   1, 2, 3, 4, 6,8, 12, 16, 24, 1, 2, 3, 4, 6,8, 12, 16, 24,  1, 2, 3, 4, 6,8, 12, 16 ]
thicknesses = [ 16, 24, 32, 48, 60, 72, 90]
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
		
		
class DoodleFrame(wx.Frame):
	def __init__(self, parent=None):
		super(DoodleFrame, self).__init__(parent, title="Doodle Frame", 
			size=wx.GetDisplaySize(), 
			style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
		doodle = DoodleWindow(self)


if __name__ == '__main__':
	app = wx.App()
	frame = DoodleFrame()
	frame.Show()
	app.MainLoop()
