# by Michał Kiedrzyński
# 11/2021

import gui
import threading


if __name__ == '__main__':
    app_thread = threading.Thread(target=gui.run)
    app_thread.start()
