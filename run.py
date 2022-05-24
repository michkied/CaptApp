# by Michał Kiedrzyński
# 11/2021

import app.gui as gui
import threading

if __name__ == '__main__':
    app_thread = threading.Thread(target=gui.run)
    app_thread.start()
