import wx
colours =  ['#e7ebee','#6c7197','#739211','#080300','#d92405','#3563eb','#eac124']
thicknesses = [6,  12, 24,12, 24,12, 24,12, 24,12, 24,12, 24, 48, 60]
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