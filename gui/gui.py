import wx
import threading
import time
import sys
import json
from .settings_menu import Settings


class Overlay(wx.Frame):
    def __init__(self):
        style = (wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                 wx.NO_BORDER | wx.FRAME_SHAPED)
        wx.Frame.__init__(self, None, title='CaptApp', style=style)
        self.SetBackgroundColour('black')

        # Retrieve saved settings
        try:
            with open('gui/settings.json', 'r', encoding='UTF-8') as f:
                data = json.loads(f.read())
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            data = {'fontSize': 15, 'transparencyValue': 175}
            with open('gui/settings.json', 'w', encoding='UTF-8') as f:
                f.write(json.dumps(data))
        self.fontsize = data['fontSize']
        self.transparency_value = data['transparencyValue']

        self.SetTransparent(self.transparency_value)

        self.init_size()

        # Create caption
        self.caption = wx.StaticText(self, label="Słucham... (wciśnij ESC by zamknąć)", style=wx.ALIGN_CENTER_HORIZONTAL, size=(self.width, self.height), pos=(0, 0))
        self.overlay_font = wx.Font(self.fontsize, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.BOLD)
        self.caption.SetForegroundColour((255, 255, 255))
        self.caption.SetFont(self.overlay_font)

        # Bind methods
        self.Bind(wx.EVT_KEY_UP, self.handle_key_press)
        self.ongoing_esc_confirmation = False

        # Save size data
        with open('temp/display_data.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps({'width': self.width, 'height': self.height}))

        # Clear output file
        with open('temp/output.txt', 'w+', encoding='UTF-8') as f:
            f.write('Słucham...\n(wciśnij ESC by zamknąć lub CTRL by wejść do ustawień)')

        # Run update_caption_loop in a thread
        thread = threading.Thread(target=self.update_caption_loop)
        thread.start()

    def init_size(self):
        # Calculate frame size & position
        d_width, d_height = wx.GetDisplaySize()

        w_width_ratio, w_height_ratio = 0.8, 0.055
        self.width = round(d_width * w_width_ratio)
        self.height = round(d_height * w_height_ratio)

        pos_y_ratio, pos_x_ratio = 0.5, 0.90
        pos_y = round(d_width * pos_y_ratio - d_width * w_width_ratio / 2)
        pos_x = round(d_height * pos_x_ratio - d_height * w_height_ratio / 2)

        # Set frame size & position
        self.SetSize(self.width, self.height)
        self.SetPosition((pos_y, pos_x))

    def handle_key_press(self, event):
        # Exit app
        if event.GetRawKeyCode() == 27:  # ESC
            if not self.ongoing_esc_confirmation:
                self.caption.SetLabel('Wciśnij ESC ponownie by zamknąć')
                self.ongoing_esc_confirmation = True
                return
            else:
                self.Close(force=True)
                sys.exit()
        self.ongoing_esc_confirmation = False

        # Open settings
        if event.GetRawKeyCode() == 17:  # CTRL
            self.menu = Settings(self)
            self.menu.Show()

    def update_caption_loop(self):
        previous_text = ''
        while True:
            if not self.ongoing_esc_confirmation:
                with open('temp/output.txt', 'r', encoding='UTF-8') as output:
                    text = output.read()

                if text != previous_text:
                    wx.CallAfter(self.caption.SetLabel, text)
                previous_text = text
            time.sleep(0.5)


def run():
    wxapp = wx.App()
    Overlay().Show()
    wxapp.MainLoop()
