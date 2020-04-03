import wx
from wx.lib import buttons # for generic button classes

#----------------------------------------------------------------------


class ControlPanel(wx.Panel):

	BMP_SIZE = 16
	BMP_BORDER = 2

	def __init__(self, parent, ID, doodle):
		wx.Panel.__init__(self, parent, ID, style=wx.RAISED_BORDER)

		numCols = 4
		spacing = 4

		btnSize = wx.Size(self.BMP_SIZE + 2*self.BMP_BORDER,
						  self.BMP_SIZE + 2*self.BMP_BORDER)

		self.clrBtns = {}
		colours = doodle.menuColours
		keys = list(colours.keys())
		keys.sort()
		cGrid = wx.GridSizer(cols=numCols, hgap=2, vgap=2)
		for k in keys:
			bmp = self.MakeBitmap(colours[k])
			b = buttons.GenBitmapToggleButton(self, k, bmp, size=btnSize )
			b.SetBezelWidth(1)
			b.SetUseFocusIndicator(False)
			self.Bind(wx.EVT_BUTTON, self.OnSetColour, b)
			cGrid.Add(b, 0)
			self.clrBtns[colours[k]] = b
		
		self.clrBtns[colours[keys[0]]].SetToggle(True)

		self.thknsBtns = {}
		tGrid = wx.GridSizer(cols=numCols, hgap=2, vgap=2)
		for x in range(1, doodle.maxThickness+1):
			b = buttons.GenToggleButton(self, x, str(x), size=btnSize)
			b.SetBezelWidth(1)
			b.SetUseFocusIndicator(False)
			self.Bind(wx.EVT_BUTTON, self.OnSetThickness, b)
			tGrid.Add(b, 0)
			self.thknsBtns[x] = b
			
		self.thknsBtns[1].SetToggle(True)


		ci = ColourIndicator(self)
		doodle.AddListener(ci)
		doodle.Notify()
		self.doodle = doodle

		box = wx.BoxSizer(wx.VERTICAL)
		box.Add(cGrid, 0, wx.ALL, spacing)
		box.Add(tGrid, 0, wx.ALL, spacing)
		box.Add(ci, 0, wx.EXPAND|wx.ALL, spacing)
		
		if 1:
			e = wx.FontEnumerator()
			e.EnumerateFacenames()
			elist= e.GetFacenames()
			self.lb1 = wx.ListBox(self, -1, wx.DefaultPosition, (200, -1),
							 elist, wx.LB_SINGLE)
			self.Bind(wx.EVT_LISTBOX, self.OnSelect, id=self.lb1.GetId())
			box.Add(self.lb1, 0, wx.EXPAND|wx.ALL)
		
		self.SetSizer(box)
		self.SetAutoLayout(True)

		# Resize this window so it is just large enough for the
		# minimum requirements of the sizer.
		box.Fit(self)
		
	def OnSelect(self, evt):
		face = self.lb1.GetStringSelection()
		print(face)
		self.doodle.setFont(face)
		



	def MakeBitmap(self, colour):
		"""
		We can create a bitmap of whatever we want by simply selecting
		it into a wx.MemoryDC and drawing on it.  In this case we just set
		a background brush and clear the dc.
		"""
		bmp = wx.Bitmap(self.BMP_SIZE, self.BMP_SIZE)
		dc = wx.MemoryDC()
		dc.SelectObject(bmp)
		dc.SetBackground(wx.Brush(colour))
		dc.Clear()
		dc.SelectObject(wx.NullBitmap)
		return bmp


	def OnSetColour(self, event):
		"""
		Use the event ID to get the colour, set that colour in the doodle.
		"""
		colour = self.doodle.menuColours[event.GetId()]
		if colour != self.doodle.colour:
			# untoggle the old colour button
			self.clrBtns[self.doodle.colour].SetToggle(False)
		# set the new colour
		self.doodle.SetColour(colour)


		


	def OnSetThickness(self, event):
		"""
		Use the event ID to set the thickness in the doodle.
		"""
		thickness = event.GetId()
		if thickness != self.doodle.thickness:
			# untoggle the old thickness button
			self.thknsBtns[self.doodle.thickness].SetToggle(False)
		# set the new colour
		self.doodle.SetThickness(thickness)



#----------------------------------------------------------------------

class ColourIndicator(wx.Window):
	"""
	An instance of this class is used on the ControlPanel to show
	a sample of what the current doodle line will look like.
	"""
	def __init__(self, parent):
		wx.Window.__init__(self, parent, -1, style=wx.SUNKEN_BORDER)
		self.SetBackgroundColour(wx.WHITE)
		self.SetMinSize( (45, 45) )
		self.colour = self.thickness = None
		self.Bind(wx.EVT_PAINT, self.OnPaint)


	def Update(self, colour, thickness):
		"""
		The doodle window calls this method any time the colour
		or line thickness changes.
		"""
		self.colour = colour
		self.thickness = thickness
		self.Refresh()  # generate a paint event


	def OnPaint(self, event):
		"""
		This method is called when all or part of the window needs to be
		redrawn.
		"""
		dc = wx.PaintDC(self)
		if self.colour:
			sz = self.GetClientSize()
			pen = wx.Pen(self.colour, self.thickness)
			#dc.BeginDrawing()
			dc.SetPen(pen)
			dc.DrawLine(10, int(sz.height/2), sz.width-10, int(sz.height/2))
			#dc.EndDrawing()

