import wx
import threading
import time
import sys


class Frame(wx.Frame):
    def __init__(self):
        style = (wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                 wx.NO_BORDER | wx.FRAME_SHAPED)
        wx.Frame.__init__(self, None, title='CaptApp', style=style)
        self.SetBackgroundColour('black')
        self.SetTransparent(175)

        # Calculate frame size & position
        d_width, d_height = wx.GetDisplaySize()

        w_width_ratio, w_height_ratio = 0.7, 0.05
        pos_y_ratio, pos_x_ratio = 0.5, 0.90

        width = int(d_width * w_width_ratio)
        height = int(d_height * w_height_ratio)

        pos_y = int(d_width * pos_y_ratio - d_width * w_width_ratio / 2)
        pos_x = int(d_height * pos_x_ratio - d_height * w_height_ratio / 2)

        # Set frame size & position
        self.SetSize(width, height)
        self.SetPosition((pos_y, pos_x))

        # Create caption
        self.caption = wx.StaticText(self, label="Słucham...", style=wx.ALIGN_CENTER_HORIZONTAL, size=(width, height), pos=(0, 0))
        font = wx.Font(wx.Size(10, int(height/3)), family=wx.DEFAULT, style=wx.NORMAL, weight=wx.BOLD)
        self.caption.SetForegroundColour((255, 255, 255))
        self.caption.SetFont(font)

        # Bind exit method to frame
        self.Bind(wx.EVT_KEY_UP, self.exit)
        self.ongoing_esc_confirmation = False

        # Run update caption loop in a thread
        thread = threading.Thread(target=self.update_caption_loop)
        thread.start()

    def exit(self, event):
        if event.GetKeyCode() == 27:  # 27 is Esc
            if not self.ongoing_esc_confirmation:
                self.caption.SetLabel('Wciśnij Esc ponownie by wyjść')
                self.ongoing_esc_confirmation = True
            else:
                self.Close(force=True)
                sys.exit()
        else:
            self.ongoing_esc_confirmation = False

    def on_click(self, event):
        print('clicked')
        self.ongoing_esc_confirmation = False

    def update_caption_loop(self):
        while True:
            if not self.ongoing_esc_confirmation:
                with open('recognition/output.txt', 'r+', encoding='UTF-8') as output:
                    text = output.read()

                wx.CallAfter(self.caption.SetLabel, text)
            time.sleep(0.5)


def run():
    wxapp = wx.App()
    f = Frame()
    f.Show()
    wxapp.MainLoop()
