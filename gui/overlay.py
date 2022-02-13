import wx
import threading
import time
import json


class Overlay(wx.Frame):
    def __init__(self, parent):
        self.p = parent

        style = (wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                 wx.NO_BORDER | wx.FRAME_SHAPED)
        wx.Frame.__init__(self, None, title=self.p.gt('CaptApp - overlay'), style=style)
        self.SetBackgroundColour('black')
        self.SetTransparent(self.p.transparency_value)

        self.init_size()

        # Create caption
        self.caption = wx.StaticText(self, label=self.p.gt("Welcome to CaptApp!\nPlay your audio and the transcription will be displayed here"), style=wx.ALIGN_CENTER_HORIZONTAL, size=(self.width, self.height), pos=(0, 0))
        self.overlay_font = wx.Font(self.p.fontsize, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.BOLD)
        self.caption.SetForegroundColour((255, 255, 255))
        self.caption.SetFont(self.overlay_font)

        # Save size data
        with open('temp/display_data.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps({'width': self.width, 'height': self.height}))

        # Clear output file
        with open('temp/output.txt', 'w+', encoding='UTF-8') as f:
            f.write(self.p.gt("Welcome to CaptApp!\nPlay your audio and the transcription will be displayed here"))

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

    def update_caption_loop(self):
        previous_text = ''
        while True:

            try:
                self.IsShown()
            except RuntimeError:
                return

            with open('temp/output.txt', 'r', encoding='UTF-8') as output:
                text = output.read()

            if text != previous_text:

                if text == '###ERROR###':
                    text = self.p.gt('An error occurred. Please check your internet connection and restart CaptApp.')
                elif text == '###CLEAR###':
                    text = self.p.gt("Welcome to CaptApp!\nPlay your audio and the transcription will be displayed here")

                wx.CallAfter(self.caption.SetLabel, text)
            previous_text = text
            time.sleep(0.25)
