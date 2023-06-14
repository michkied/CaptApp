import wx
import threading
import time
import datetime

from ..recognition import recognition


class Overlay(wx.Frame):
    def __init__(self, parent):
        self.p = parent

        style = (wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                 wx.NO_BORDER | wx.FRAME_SHAPED)
        wx.Frame.__init__(self, None, title=self.p.gt('CaptApp - overlay'), style=style)
        self.SetBackgroundColour('black')
        self.SetTransparent(self.p.settings.transparency_value)

        self.init_size()
        self.p.settings.overlay_width, self.p.settings.overlay_height = self.width, self.height

        if self.p.settings.display_welcome_message:
            self.welcome_text = self.p.gt(self.p.welcome_text)
        else:
            self.welcome_text = ' '
        self.error_text = 'An error occurred. Please check your internet connection and restart CaptApp.'

        # Create caption
        self.caption = wx.StaticText(
            self,
            label=self.welcome_text,
            style=wx.ALIGN_CENTER_HORIZONTAL, size=(self.width, self.height), pos=(0, 0)
        )
        self.overlay_font = wx.Font(self.p.settings.font_size, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.BOLD)
        self.caption.SetForegroundColour((255, 255, 255))
        self.caption.SetFont(self.overlay_font)

        self.to_display = self.welcome_text

        if self.p.settings.save_caption_to_file:
            with open('app/.saved_caption/output.txt', 'a+', encoding='UTF-8') as f:
                f.write(
                    f'\n\n------------ {datetime.datetime.now().strftime("%H:%M:%S  %d/%m/%Y")}\n\n'
                )

        # Run update_caption_loop in a thread
        recognition_thread = threading.Thread(target=recognition.Recognition(self).recognition_loop)
        recognition_thread.start()
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

            text = self.to_display
            if text != previous_text:
                wx.CallAfter(self.caption.SetLabel, text)

                if self.p.settings.save_caption_to_file:
                    if text not in (self.welcome_text, self.p.gt(self.error_text)):

                        with open('app/.saved_caption/output.txt', 'a+', encoding='UTF-8') as f:
                            if text.split('\n')[0] == previous_text:
                                f.write(text.split('\n')[1]+'\n')
                            else:
                                f.write(text+'\n')

            previous_text = text
            time.sleep(0.25)
