import wx
import json


class Settings(wx.Frame):
    def __init__(self, overlay):

        self.gt = overlay.gt

        self.overlay_frame = overlay
        wx.Frame.__init__(self, None, title=self.gt('CaptApp - settings'))
        self.SetBackgroundColour('black')
        self.Center(wx.BOTH)
        self.SetIcon(wx.Icon("gui/resources/icon.ico"))

        menu_font = wx.Font(13, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.BOLD)

        # Create settings menu elements

        self.fontsize_text = wx.StaticText(self, label=self.gt("Font size"), style=wx.ALIGN_CENTER_HORIZONTAL, pos=(0, 0))
        self.fontsize_text.SetForegroundColour((255, 255, 255))
        self.fontsize_text.SetFont(menu_font)

        self.fontsizeSlider = wx.Slider(self, minValue=5, maxValue=50, size=(400, -1), style=wx.SL_AUTOTICKS, id=1000, value=self.overlay_frame.fontsize)
        self.fontsizeSlider.SetTick(45)

        self.transparency_text = wx.StaticText(self, label=self.gt("Window transparency"), style=wx.ALIGN_CENTER_HORIZONTAL, pos=(0, 0))
        self.transparency_text.SetForegroundColour((255, 255, 255))
        self.transparency_text.SetFont(menu_font)

        self.transparencySlider = wx.Slider(self, minValue=10, maxValue=255, size=(400, 50), id=1001, value=self.overlay_frame.transparency_value)

        # Align elements
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.fontsize_text, 0, wx.LEFT | wx.RIGHT | wx.TOP, 20)
        sizer.Add(self.fontsizeSlider, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)
        sizer.Add(self.transparency_text, 0, wx.LEFT | wx.RIGHT | wx.TOP, 20)
        sizer.Add(self.transparencySlider, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)
        self.SetSizer(sizer)

        # Bind methods
        self.Bind(wx.EVT_SCROLL, self.update_font_size, id=1000)
        self.Bind(wx.EVT_SCROLL, self.update_transparency, id=1001)
        self.Bind(wx.EVT_CLOSE, self.save_and_exit)

    # Handle font size slider
    def update_font_size(self, args):
        value = self.fontsizeSlider.GetValue()
        self.overlay_frame.fontsize = value
        self.overlay_frame.overlay_font.SetPointSize(value)
        self.overlay_frame.caption.SetFont(self.overlay_frame.overlay_font)

    # Handle transparency slider
    def update_transparency(self, args):
        value = self.transparencySlider.GetValue()
        self.overlay_frame.transparency_value = value
        self.overlay_frame.SetTransparent(value)

    def save_and_exit(self, args):

        data = {'fontSize': self.overlay_frame.fontsize,
                'transparencyValue': self.overlay_frame.transparency_value,
                'language': self.overlay_frame.language}

        with open('gui/settings.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(data))

        self.Destroy()
