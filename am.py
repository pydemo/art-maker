# superdoodle.py
"""
This module implements the SuperDoodle demo application.  It takes the
DoodleWindow previously presented and reuses it in a much more
intelligent Frame.  This one has a menu and a statusbar, is able to
save and reload doodles, clear the workspace, and has a simple control
panel for setting color and line thickness in addition to the popup
menu that DoodleWindow provides.  There is also a nice About dialog
implmented using an wx.html.HtmlWindow.
"""
import wx
import sys, os
import _pickle as cPickle


from include.DoodleFrame import DoodleFrame



from wx.lib.mixins.inspection import InspectionMixin
from wx.lib.softwareupdate import SoftwareUpdate

#----------------------------------------------------------------------
#----------------------------------------------------------------------

class DoodleApp(wx.App, InspectionMixin, SoftwareUpdate):
	def OnInit(self):
		BASEURL='http://wxPython.org/software-update-test/'
		self.InitUpdates(BASEURL, 
						 BASEURL + 'ChangeLog.txt',
						 icon=wx.Icon(r'images\mondrian.ico'))
		self.Init() # for InspectionMixin
		
		frame = DoodleFrame(None)
		frame.Show(True)
		self.SetTopWindow(frame)
		self.SetAppDisplayName('SuperDoodle')
		return True

#----------------------------------------------------------------------

if __name__ == '__main__':
	app = DoodleApp(redirect=False)
	app.MainLoop()
	
