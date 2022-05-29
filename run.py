# by Michał Kiedrzyński
# 11/2021

from app.gui.menu import run
import threading

if __name__ == '__main__':
    app_thread = threading.Thread(target=run)
    app_thread.start()
