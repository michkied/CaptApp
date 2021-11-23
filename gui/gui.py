import wx
import threading
import time
import sys
import json


class Frame(wx.Frame):
    def __init__(self):
        style = (wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                 wx.NO_BORDER | wx.FRAME_SHAPED)
        wx.Frame.__init__(self, None, title='CaptApp', style=style)
        self.SetBackgroundColour('black')
        self.SetTransparent(175)

        # Bind exit method to frame
        self.Bind(wx.EVT_KEY_UP, self.exit)
        self.ongoing_esc_confirmation = False

        self.init_size()

        # Create caption
        self.fontsize = 18
        self.caption = wx.StaticText(self, label="Słucham... (wciśnij ESC by zamknąć)", style=wx.ALIGN_CENTER_HORIZONTAL, size=(self.width, self.height), pos=(0, 0))
        font = wx.Font(self.fontsize, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.BOLD)
        self.caption.SetForegroundColour((255, 255, 255))
        self.caption.SetFont(font)

        # Save size data
        with open('gui/display_data.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps({'width': self.width, 'height': self.height, 'fontsize': self.fontsize}))

        # Clear output file
        with open('recognition/output.txt', 'w+', encoding='UTF-8') as f:
            f.write('Słucham... (wciśnij ESC by zamknąć)')

        # Run update_caption_loop in a thread
        thread = threading.Thread(target=self.update_caption_loop)
        thread.start()

    def init_size(self):
        # Calculate frame size & position
        d_width, d_height = wx.GetDisplaySize()

        w_width_ratio, w_height_ratio = 0.8, 0.055
        self.width = int(d_width * w_width_ratio)
        self.height = int(d_height * w_height_ratio)

        pos_y_ratio, pos_x_ratio = 0.5, 0.90
        pos_y = int(d_width * pos_y_ratio - d_width * w_width_ratio / 2)
        pos_x = int(d_height * pos_x_ratio - d_height * w_height_ratio / 2)

        # Set frame size & position
        self.SetSize(self.width, self.height)
        self.SetPosition((pos_y, pos_x))

    def exit(self, event):
        if event.GetKeyCode() == 27:
            if not self.ongoing_esc_confirmation:
                self.caption.SetLabel('Wciśnij ESC ponownie by zamknąć')
                self.ongoing_esc_confirmation = True
            else:
                self.Close(force=True)
                sys.exit()
        else:
            self.ongoing_esc_confirmation = False

    def update_caption_loop(self):
        previous_text = ''
        while True:
            if not self.ongoing_esc_confirmation:
                with open('recognition/output.txt', 'r', encoding='UTF-8') as output:
                    text = output.read()

                if text != previous_text:
                    wx.CallAfter(self.caption.SetLabel, text)
                previous_text = text
            time.sleep(0.5)


def run():
    wxapp = wx.App()
    Frame().Show()
    wxapp.MainLoop()
