import wx
#----------------------------------------------------------------------

class DoodleAbout(wx.Dialog):
	""" An about box that uses an HTML window """

	text = '''
<html>
<body bgcolor="#ACAA60">
<center><table bgcolor="#455481" width="100%%" cellspacing="0"
cellpadding="0" border="1">
<tr>
	<td align="center"><h1>Art Maker %s</h1></td>
</tr>
</table>
</center>
<p><b>ArtMaker</b> is a doodler for artist that
will hopefully give inspiration or two. 
</body>
</html>
''' 

	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, -1, 'About SuperDoodle',
						  size=(420, 380) )

		html = wx.html.HtmlWindow(self, -1)
		import version
		html.SetPage(self.text % version.VERSION)
		button = wx.Button(self, wx.ID_OK, "Okay")

		# constraints for the html window
		lc = wx.LayoutConstraints()
		lc.top.SameAs(self, wx.Top, 5)
		lc.left.SameAs(self, wx.Left, 5)
		lc.bottom.SameAs(button, wx.Top, 5)
		lc.right.SameAs(self, wx.Right, 5)
		html.SetConstraints(lc)

		# constraints for the button
		lc = wx.LayoutConstraints()
		lc.bottom.SameAs(self, wx.Bottom, 5)
		lc.centreX.SameAs(self, wx.CentreX)
		lc.width.AsIs()
		lc.height.AsIs()
		button.SetConstraints(lc)

		self.SetAutoLayout(True)
		self.Layout()
		self.CentreOnParent(wx.BOTH)
