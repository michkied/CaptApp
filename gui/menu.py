import wx
import sys
import json
import gettext

from .settings import Settings
from .overlay import Overlay


class Menu(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='CaptApp', size=(400, 500))
        self.SetBackgroundColour('white')

        self.Center(wx.BOTH)
        self.SetIcon(wx.Icon("gui/resources/icon.ico"))

        menu_font14 = wx.Font(14, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.BOLD)

        # Retrieve saved settings
        try:
            with open('gui/settings.json', 'r', encoding='UTF-8') as f:
                settings = json.loads(f.read())
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            settings = {'fontSize': 16, 'transparencyValue': 175, 'interfaceLang': 'en', 'audioLang': 'en'}
            with open('gui/settings.json', 'w', encoding='UTF-8') as f:
                f.write(json.dumps(settings))
        self.fontsize = settings['fontSize']
        self.transparency_value = settings['transparencyValue']
        self.interface_language = settings['interfaceLang']
        self.audio_language = settings['audioLang']

        # Support multiple interface languages
        self.pl = gettext.translation('strings', localedir='locales', languages=['pl'])
        self.pl.install()
        self.en = gettext.translation('strings', localedir='locales', languages=['en'])
        self.en.install()
        if self.interface_language == 'pl':
            self.gt = self.pl.gettext
        else:
            self.gt = self.en.gettext

        # Initiate GUI
        main_vertical_sizer = wx.BoxSizer(wx.VERTICAL)

        self.logo_bitmap = wx.StaticBitmap(self, bitmap=wx.Bitmap(wx.Image('gui/resources/logo.png').Scale(170, 170, wx.IMAGE_QUALITY_HIGH)))
        main_vertical_sizer.Add(self.logo_bitmap, 0, wx.ALIGN_CENTER | wx.TOP, 30)

        column1 = wx.BoxSizer(wx.VERTICAL)

        self.run_overlay_button = wx.Button(self, id=100, size=(100, 100))
        self.run_overlay_button.SetBitmap(wx.Bitmap(wx.Image('gui/resources/run.png').Scale(70, 70, wx.IMAGE_QUALITY_HIGH)))
        self.run_overlay_button.SetDefault()
        column1.Add(self.run_overlay_button, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        self.run_label = wx.StaticText(self, label=self.gt("Run"), style=wx.ALIGN_CENTER)
        self.run_label.SetFont(menu_font14)
        column1.Add(self.run_label, 0, wx.ALIGN_CENTER)

        column2 = wx.BoxSizer(wx.VERTICAL)

        self.open_settings_button = wx.Button(self, id=101, size=(100, 100))
        self.open_settings_button.SetBitmap(wx.Bitmap(wx.Image('gui/resources/settings.png').Scale(70, 70, wx.IMAGE_QUALITY_HIGH)))
        column2.Add(self.open_settings_button, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        self.open_settings_label = wx.StaticText(self, label=self.gt("Settings"), style=wx.ALIGN_CENTER)
        self.open_settings_label.SetFont(menu_font14)
        column2.Add(self.open_settings_label, 0, wx.ALIGN_CENTER)

        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.Add(column1, 0, wx.ALIGN_CENTER | wx.RIGHT | wx.LEFT, 15)
        row1.Add(column2, 0, wx.ALIGN_CENTER | wx.RIGHT | wx.LEFT, 15)

        main_vertical_sizer.Add(row1, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 30)

        self.SetSizer(main_vertical_sizer)

        self.Bind(wx.EVT_BUTTON, self.run_overlay, id=100)
        self.Bind(wx.EVT_BUTTON, self.open_settings, id=101)
        self.Bind(wx.EVT_CLOSE, self.close)

    def run_overlay(self, event):
        try:
            self.overlay.IsShown()
        except (AttributeError, RuntimeError):
            self.overlay = Overlay(self)
            self.overlay.Show()
        self.overlay.SetFocus()

    def open_settings(self, event):
        try:
            self.settings.IsShown()
        except (AttributeError, RuntimeError):
            self.settings = Settings(self)
            self.settings.Show()
        self.settings.SetFocus()

    def close(self, event):
        sys.exit()


def run():
    wxapp = wx.App()
    Menu().Show()
    wxapp.MainLoop()
