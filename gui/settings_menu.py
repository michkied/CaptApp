import wx
import wx.adv
import json


class Settings(wx.Frame):
    def __init__(self, parent):
        self.p = parent

        wx.Frame.__init__(self, None, title=self.p.gt('CaptApp - settings'), size=(450, 600))
        self.SetBackgroundColour('white')

        self.Center(wx.BOTH)
        self.SetIcon(wx.Icon("gui/resources/icon.ico"))

        menu_font14 = wx.Font(14, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.BOLD)
        menu_font12 = wx.Font(12, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL)

        # Create settings menu elements

        self.logo_bitmap = wx.StaticBitmap(self, bitmap=wx.Bitmap(wx.Image('gui/resources/icon.ico').Scale(170, 170, wx.IMAGE_QUALITY_HIGH)))

        self.fontsize_label = wx.StaticText(self, label=self.p.gt("Font size"), style=wx.ALIGN_CENTER)
        self.fontsize_label.SetForegroundColour((0, 0, 0))
        self.fontsize_label.SetBackgroundColour((255, 255, 255))
        self.fontsize_label.SetFont(menu_font14)

        self.fontsizeSlider = wx.Slider(self, minValue=5, maxValue=50, size=(400, 40), style=wx.SL_AUTOTICKS, id=1000, value=self.p.fontsize)
        self.fontsizeSlider.SetBackgroundColour((255, 255, 255))

        self.transparency_label = wx.StaticText(self, label=self.p.gt("Window transparency"), style=wx.ALIGN_CENTER)
        self.transparency_label.SetForegroundColour((0, 0, 0))
        self.transparency_label.SetBackgroundColour((255, 255, 255))
        self.transparency_label.SetFont(menu_font14)

        self.transparencySlider = wx.Slider(self, minValue=10, maxValue=255, size=(400, 40), id=1001, value=self.p.transparency_value)
        self.transparencySlider.SetBackgroundColour((255, 255, 255))

        self.interface_language_label = wx.StaticText(self, label=self.p.gt("Interface language"), style=wx.ALIGN_CENTER)
        self.interface_language_label.SetForegroundColour((0, 0, 0))
        self.interface_language_label.SetBackgroundColour((255, 255, 255))
        self.interface_language_label.SetFont(menu_font14)

        languages = ['English', 'Polski']
        if self.p.language == 'pl':
            lang_text = languages[1]
        else:
            lang_text = languages[0]
        self.interface_language_list = wx.adv.OwnerDrawnComboBox(self, style=(wx.LB_SINGLE | wx.LB_OWNERDRAW), choices=languages, id=1002, value=lang_text, size=(150, -1))
        self.interface_language_list.SetFont(menu_font12)
        self.interface_language_list.SetBackgroundColour((255, 255, 255))
        self.interface_language_list.SetForegroundColour((0, 0, 0))
        self.interface_language_list.SetTransparent(70)

        # Align elements
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.logo_bitmap, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 30)
        sizer.Add(self.fontsize_label, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 30)
        sizer.Add(self.fontsizeSlider, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)
        sizer.Add(self.transparency_label, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT | wx.TOP, 30)
        sizer.Add(self.transparencySlider, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)
        sizer.Add(self.interface_language_label, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT | wx.TOP, 20)
        sizer.Add(self.interface_language_list, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        self.SetSizer(sizer)

        # Bind methods
        self.Bind(wx.EVT_SCROLL, self.update_font_size, id=1000)
        self.Bind(wx.EVT_SCROLL, self.update_transparency, id=1001)
        self.Bind(wx.EVT_COMBOBOX, self.update_interface_language, id=1002)
        self.Bind(wx.EVT_CLOSE, self.save_and_exit)

    # Handle font size slider
    def update_font_size(self, args):
        value = self.fontsizeSlider.GetValue()
        self.p.fontsize = value
        self.p.overlay_font.SetPointSize(value)
        self.p.caption.SetFont(self.p.overlay_font)

    # Handle transparency slider
    def update_transparency(self, args):
        value = self.transparencySlider.GetValue()
        self.p.transparency_value = value
        self.p.SetTransparent(value)

    # Handle interface language changes
    def update_interface_language(self, args):
        value = self.interface_language_list.GetValue()
        if value == 'Polski':
            self.p.language = 'pl'
            self.p.gt = self.p.pl.gettext
        else:
            self.p.language = 'en'
            self.p.gt = self.p.en.gettext

        with open('temp/output.txt', 'w+', encoding='UTF-8') as f:
            f.write(self.p.gt("Listening...\n(press ESC to exit or CTRL to open settings)"))

        self.fontsize_label.SetLabel(self.p.gt("Font size"))
        self.transparency_label.SetLabel(self.p.gt('Window transparency'))
        self.interface_language_label.SetLabel(self.p.gt('Interface language'))

        self.Layout()

    def save_and_exit(self, args):
        data = {'fontSize': self.p.fontsize,
                'transparencyValue': self.p.transparency_value,
                'language': self.p.language}

        with open('gui/settings.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(data))

        self.Destroy()
