import app
import recognition
import threading


if __name__ == '__main__':
    app_thread = threading.Thread(target=app.run)
    app_thread.start()

    recognition_thread = threading.Thread(target=recognition.recognise_loop)
    recognition_thread.start()
