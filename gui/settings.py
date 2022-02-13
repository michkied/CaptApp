import wx
import wx.adv
import json

from .languages import interface_languages, audio_languages


class Settings(wx.Frame):
    def __init__(self, parent):
        self.p = parent

        wx.Frame.__init__(self, None, title=self.p.gt('CaptApp - settings'), size=(450, 650))
        self.SetBackgroundColour('white')

        self.Center(wx.BOTH)
        self.SetIcon(wx.Icon("gui/resources/icon.ico"))

        menu_font22 = wx.Font(22, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.BOLD)
        menu_font14 = wx.Font(14, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.BOLD)
        menu_font12 = wx.Font(12, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL)

        # Create settings menu elements

        self.settings_bitmap = wx.StaticBitmap(self, bitmap=wx.Bitmap(wx.Image('gui/resources/settings.png').Scale(150, 150, wx.IMAGE_QUALITY_HIGH)))
        self.settings_label = wx.StaticText(self, label=self.p.gt("Settings"), style=wx.ALIGN_CENTER)
        self.settings_label.SetFont(menu_font22)

        self.fontsize_label = wx.StaticText(self, label=self.p.gt("Font size"), style=wx.ALIGN_CENTER)
        self.fontsize_label.SetFont(menu_font14)

        self.fontsizeSlider = wx.Slider(self, minValue=5, maxValue=50, size=(400, 40), style=wx.SL_AUTOTICKS, id=1000, value=self.p.fontsize)
        self.fontsizeSlider.SetBackgroundColour((255, 255, 255))

        self.transparency_label = wx.StaticText(self, label=self.p.gt("Window transparency"), style=wx.ALIGN_CENTER)
        self.transparency_label.SetFont(menu_font14)

        self.transparencySlider = wx.Slider(self, minValue=10, maxValue=255, size=(400, 40), id=1001, value=self.p.transparency_value)
        self.transparencySlider.SetBackgroundColour((255, 255, 255))

        # Interface language
        self.interface_language_label = wx.StaticText(self, label=self.p.gt("Interface language"), style=wx.ALIGN_CENTER)
        self.interface_language_label.SetFont(menu_font14)

        lang_text = interface_languages[self.p.interface_language]
        self.interface_language_list = wx.adv.OwnerDrawnComboBox(self, style=(wx.LB_SINGLE | wx.LB_OWNERDRAW), choices=list(interface_languages.values()), id=1002, value=lang_text, size=(150, -1))
        self.interface_language_list.SetFont(menu_font12)
        self.interface_language_list.SetBackgroundColour((255, 255, 255))
        self.interface_language_list.SetForegroundColour((0, 0, 0))
        self.interface_language_list.SetTransparent(70)

        # Audio language
        self.audio_language_label = wx.StaticText(self, label=self.p.gt("Audio language"), style=wx.ALIGN_CENTER)
        self.audio_language_label.SetFont(menu_font14)

        lang_text = list(audio_languages.keys())[list(audio_languages.values()).index(self.p.audio_language)]
        self.audio_language_list = wx.adv.OwnerDrawnComboBox(self, style=(wx.LB_SINGLE | wx.LB_OWNERDRAW), choices=list(audio_languages.keys()), id=1003, value=lang_text, size=(150, -1))
        self.audio_language_list.SetFont(menu_font12)
        self.audio_language_list.SetBackgroundColour((255, 255, 255))
        self.audio_language_list.SetForegroundColour((0, 0, 0))
        self.audio_language_list.SetTransparent(70)

        # Align elements
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.settings_bitmap, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        sizer.Add(self.settings_label, 0, wx.ALIGN_CENTER | wx.BOTTOM, 40)
        sizer.Add(self.fontsize_label, 0, wx.ALIGN_CENTER, 0)
        sizer.Add(self.fontsizeSlider, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)
        sizer.Add(self.transparency_label, 0, wx.ALIGN_CENTER | wx.TOP, 30)
        sizer.Add(self.transparencySlider, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 30)
        sizer.Add(self.interface_language_label, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        sizer.Add(self.interface_language_list, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        sizer.Add(self.audio_language_label, 0, wx.ALIGN_CENTER | wx.TOP, 25)
        sizer.Add(self.audio_language_list, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        self.SetSizer(sizer)

        # Bind methods
        self.Bind(wx.EVT_SCROLL, self.update_font_size, id=1000)
        self.Bind(wx.EVT_SCROLL, self.update_transparency, id=1001)
        self.Bind(wx.EVT_COMBOBOX, self.update_interface_language, id=1002)
        self.Bind(wx.EVT_COMBOBOX, self.update_audio_language, id=1003)
        self.Bind(wx.EVT_CLOSE, self.exit)

    # Handle font size slider
    def update_font_size(self, args):
        value = self.fontsizeSlider.GetValue()
        self.p.fontsize = value
        try:
            self.p.overlay.overlay_font.SetPointSize(value)
            self.p.overlay.caption.SetFont(self.p.overlay.overlay_font)
        except AttributeError:
            pass

    # Handle transparency slider
    def update_transparency(self, args):
        value = self.transparencySlider.GetValue()
        self.p.transparency_value = value
        try:
            self.p.overlay.SetTransparent(value)
        except AttributeError:
            pass

    # Handle interface language changes
    def update_interface_language(self, args):
        value = self.interface_language_list.GetValue()
        if value == 'Polski':
            self.p.interface_language = 'pl'
            self.p.gt = self.p.pl.gettext
        else:
            self.p.interface_language = 'en'
            self.p.gt = self.p.en.gettext

        with open('temp/output.txt', 'w+', encoding='UTF-8') as f:
            f.write(self.p.gt("Welcome to CaptApp!\nPlay your audio and the transcription will be displayed here"))

        self.settings_label.SetLabel(self.p.gt("Settings"))
        self.fontsize_label.SetLabel(self.p.gt("Font size"))
        self.transparency_label.SetLabel(self.p.gt('Window transparency'))
        self.interface_language_label.SetLabel(self.p.gt('Interface language'))
        self.audio_language_label.SetLabel(self.p.gt("Audio language"))

        if self.p.is_toggle_run:
            self.p.toggle_label.SetLabel(self.p.gt("Run"))
        else:
            self.p.toggle_label.SetLabel(self.p.gt("Stop"))
        self.p.open_settings_label.SetLabel(self.p.gt("Settings"))

        self.Layout()
        self.p.Layout()

    def update_audio_language(self, args):
        value = self.audio_language_list.GetValue()
        self.p.audio_language = audio_languages[value]
        self.save()

    def save(self):
        data = {'fontSize': self.p.fontsize,
                'transparencyValue': self.p.transparency_value,
                'interfaceLang': self.p.interface_language,
                'audioLang': self.p.audio_language}

        with open('gui/settings.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(data))

    def exit(self, args):
        self.save()
        self.Destroy()
