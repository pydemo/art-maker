
import wx    
import wx.html

import sys

from include.DoodleWindow import DoodleWindow

from include.DoodleAbout import DoodleAbout

from include.ControlPanel import ControlPanel




#----------------------------------------------------------------------

# There are standard IDs for the menu items we need in this app, or we
# could have used wx.NewId() to autogenerate some new unique ID values
# instead.

idNEW    = wx.ID_NEW
idOPEN   = wx.ID_OPEN
idSAVE   = wx.ID_SAVE
idSAVEAS = wx.ID_SAVEAS
idCLEAR  = wx.ID_CLEAR
idEXIT   = wx.ID_EXIT
idABOUT  = wx.ID_ABOUT



class DoodleFrame(wx.Frame):
	"""
	A DoodleFrame contains a DoodleWindow and a ControlPanel and manages
	their layout with a wx.BoxSizer.  A menu and associated event handlers
	provides for saving a doodle to a file, etc.
	"""
	title = "Art Maker"
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, -1, self.title, size=(800,600),
						 style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
		self.SetIcon(wx.Icon(r'images\mondrian.ico'))
		self.CreateStatusBar()
		self.MakeMenu()
		self.filename = None

		self.doodle = DoodleWindow(self, -1)
		cPanel = ControlPanel(self, -1, self.doodle)

		# Create a sizer to layout the two windows side-by-side.
		# Both will grow vertically, the doodle window will grow
		# horizontally as well.
		box = wx.BoxSizer(wx.HORIZONTAL)
		box.Add(cPanel, 0, wx.EXPAND)
		box.Add(self.doodle, 1, wx.EXPAND)

		# Tell the frame that it should layout itself in response to
		# size events using this sizer.
		self.SetSizer(box)


	def SaveFile(self):
		if self.filename:
			data = self.doodle.GetLinesData()
			with open(self.filename, 'wb') as fh:
				cPickle.dump(data, fh)
			


	def ReadFile(self):
		if self.filename:
			try:
				with open(self.filename, 'rb') as fh:
					data = cPickle.load(fh)
				
				self.doodle.SetLinesData(data)
			except cPickle.UnpicklingError:
				raise
				wx.MessageBox("%s is not a doodle file." % self.filename,
							 "oops!", style=wx.OK|wx.ICON_EXCLAMATION)


	def MakeMenu(self):
		# create the file menu
		menu1 = wx.Menu()

		# Using the "\tKeyName" syntax automatically creates a
		# wx.AcceleratorTable for this frame and binds the keys to
		# the menu items.
		menu1.Append(idOPEN, "&Open\tCtrl-O", "Open a doodle file")
		menu1.Append(idSAVE, "&Save\tCtrl-S", "Save the doodle")
		menu1.Append(idSAVEAS, "Save &As", "Save the doodle in a new file")
		menu1.AppendSeparator()
		menu1.Append(idCLEAR, "&Clear", "Clear the current doodle")
		menu1.AppendSeparator()
		menu1.Append(idEXIT, "E&xit", "Terminate the application")

		# and the help menu
		menu2 = wx.Menu()
		if hasattr(sys, 'frozen'):
			item = menu2.Append(-1, "Check for Update...")
			self.Bind(wx.EVT_MENU, self.OnMenuCheckForUpdate, item)
			
		menu2.Append(idABOUT, "&About\tCtrl-H", "Display the gratuitous 'about this app' thingamajig")

		# and add them to a menubar
		menuBar = wx.MenuBar()
		menuBar.Append(menu1, "&File")
		menuBar.Append(menu2, "&Help")
		self.SetMenuBar(menuBar)

		self.Bind(wx.EVT_MENU,   self.OnMenuOpen, id=idOPEN)
		self.Bind(wx.EVT_MENU,   self.OnMenuSave, id=idSAVE)
		self.Bind(wx.EVT_MENU, self.OnMenuSaveAs, id=idSAVEAS)
		self.Bind(wx.EVT_MENU,  self.OnMenuClear, id=idCLEAR)
		self.Bind(wx.EVT_MENU,   self.OnMenuExit, id=idEXIT)
		self.Bind(wx.EVT_MENU,  self.OnMenuAbout, id=idABOUT)



	wildcard = "Doodle files (*.ddl)|*.ddl|All files (*.*)|*.*"

	def OnMenuOpen(self, event):
		dlg = wx.FileDialog(self, "Open doodle file...", os.getcwd(),
						   style=wx.FD_OPEN, wildcard = self.wildcard)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetPath()
			self.ReadFile()
			self.SetTitle(self.title + ' -- ' + self.filename)
		dlg.Destroy()


	def OnMenuSave(self, event):
		if not self.filename:
			self.OnMenuSaveAs(event)
		else:
			self.SaveFile()


	def OnMenuSaveAs(self, event):
		dlg = wx.FileDialog(self, "Save doodle as...", os.getcwd(),
						   style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
						   wildcard = self.wildcard)
		if dlg.ShowModal() == wx.ID_OK:
			filename = dlg.GetPath()
			if not os.path.splitext(filename)[1]:
				filename = filename + '.ddl'
			self.filename = filename
			self.SaveFile()
			self.SetTitle(self.title + ' -- ' + self.filename)
		dlg.Destroy()


	def OnMenuClear(self, event):
		self.doodle.SetLinesData([])
		self.SetTitle(self.title)


	def OnMenuExit(self, event):
		self.Close()


	def OnMenuAbout(self, event):
		dlg = DoodleAbout(self)
		dlg.ShowModal()
		dlg.Destroy()

	def OnMenuCheckForUpdate(self, event):
		wx.GetApp().CheckForUpdate(parentWindow=self)