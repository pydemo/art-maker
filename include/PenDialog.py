import wx

#---------------------------------------------------------------------------
# Just A Dialog To Select Pen Styles
#---------------------------------------------------------------------------
class PenDialog(wx.Dialog):

    def __init__(self, parent=None, id=-1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE, oldpen=None,
                 pentype=0):

        wx.Dialog.__init__(self, parent, id, title, pos, size, style)

        self.colourbutton = csel.ColourSelect(self)
        self.spinwidth = wx.SpinCtrl(self, -1, "1", min=1, max=3, style=wx.SP_ARROW_KEYS)

        self.combostyle = wx.ComboBox(self, -1, choices=penstyle, style=wx.CB_DROPDOWN|wx.CB_READONLY)

        choices = ["[1, 1]", "[2, 2]", "[3, 3]", "[4, 4]"]
        self.combodash = wx.ComboBox(self, -1, choices=choices, style=wx.CB_DROPDOWN|wx.CB_READONLY)

        self.okbutton = wx.Button(self, wx.ID_OK)
        self.cancelbutton = wx.Button(self, wx.ID_CANCEL)

        self.oldpen = oldpen
        self.parent = parent
        self.pentype = pentype

        self.SetProperties()
        self.DoLayout()

        self.Bind(wx.EVT_COMBOBOX, self.OnStyle, self.combostyle)
        self.Bind(wx.EVT_BUTTON, self.OnOk, self.okbutton)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelbutton)


    def SetProperties(self):

        self.SetTitle("Pen Dialog Selector")
        self.colourbutton.SetMinSize((25, 25))
        self.colourbutton.SetColour(self.oldpen.GetColour())

        style = self.oldpen.GetStyle()
        for count, st in enumerate(penstyle):
            if eval(st) == style:
                self.combostyle.SetSelection(count)
                if count == 5:
                    self.combodash.Enable(True)
                else:
                    self.combodash.Enable(False)
                break

        if self.combodash.IsEnabled():
            dashes = repr(self.oldpen.GetDashes())
            self.combodash.SetValue(dashes)

        self.spinwidth.SetValue(self.oldpen.GetWidth())
        self.okbutton.SetDefault()

        if self.pentype == 1:
            self.spinwidth.Enable(False)


    def DoLayout(self):

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        bottomsizer = wx.BoxSizer(wx.HORIZONTAL)
        middlesizer = wx.BoxSizer(wx.VERTICAL)
        stylesizer = wx.BoxSizer(wx.HORIZONTAL)
        widthsizer = wx.BoxSizer(wx.HORIZONTAL)
        coloursizer = wx.BoxSizer(wx.HORIZONTAL)
        label_1 = wx.StaticText(self, -1, "Please Choose The Pen Settings:")
        label_1.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        mainsizer.Add(label_1, 0, wx.ALL|wx.ADJUST_MINSIZE, 10)
        label_2 = wx.StaticText(self, -1, "Pen Colour")
        coloursizer.Add(label_2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        coloursizer.Add((5, 5), 1, wx.ADJUST_MINSIZE, 0)
        coloursizer.Add(self.colourbutton, 0, wx.ALL|wx.ADJUST_MINSIZE, 5)
        middlesizer.Add(coloursizer, 0, wx.EXPAND, 0)
        label_3 = wx.StaticText(self, -1, "Pen Width")
        widthsizer.Add(label_3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        widthsizer.Add((5, 5), 1, wx.ADJUST_MINSIZE, 0)
        widthsizer.Add(self.spinwidth, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        middlesizer.Add(widthsizer, 0, wx.EXPAND, 0)
        label_4 = wx.StaticText(self, -1, "Pen Style")
        stylesizer.Add(label_4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        stylesizer.Add((5, 5), 1, wx.ADJUST_MINSIZE, 0)
        stylesizer.Add(self.combostyle, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        stylesizer.Add(self.combodash, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        middlesizer.Add(stylesizer, 0, wx.BOTTOM|wx.EXPAND, 5)
        mainsizer.Add(middlesizer, 1, wx.EXPAND, 0)
        bottomsizer.Add(self.okbutton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 20)
        bottomsizer.Add((20, 20), 1, wx.ADJUST_MINSIZE, 0)
        bottomsizer.Add(self.cancelbutton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 20)
        mainsizer.Add(bottomsizer, 0, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        mainsizer.SetSizeHints(self)
        self.Layout()
        self.Centre()


    def OnStyle(self, event):

        choice = event.GetEventObject().GetValue()
        self.combodash.Enable(choice==5)
        event.Skip()


    def OnOk(self, event):

        colour = self.colourbutton.GetColour()
        style = eval(self.combostyle.GetValue())
        width = int(self.spinwidth.GetValue())

        dashes = None
        if self.combostyle.GetSelection() == 5:
            dashes = eval(self.combodash.GetValue())

        pen = wx.Pen(colour, width, style)

        if dashes:
            pen.SetDashes(dashes)

        pen.SetCap(wx.CAP_BUTT)

        if self.pentype == 0:
            self.parent.SetConnectionPen(pen)
        else:
            self.parent.SetBorderPen(pen)

        self.Destroy()
        event.Skip()


    def OnCancel(self, event):

        self.Destroy()
        event.Skip()
