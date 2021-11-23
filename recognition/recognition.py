import time
import speech_recognition as sr
import json
import threading

r = sr.Recognizer()
r.pause_threshold = 0.5

# print(sr.Microphone.list_microphone_names())


def clear_output():
    with open('recognition/output.txt', 'w', encoding='UTF-8') as f:
        f.write('Słucham... (wciśnij ESC by zamknąć)')


def wrapping(text_to_wrap):
    # Get display data
    with open('gui/display_data.json', 'r', encoding='UTF-8') as f:
        data = json.loads(f.read())
    num_of_chars = int(data['width'] / (data['fontsize'] * 0.75))

    lines = []
    while len(text_to_wrap) > num_of_chars:
        chunk = text_to_wrap[:num_of_chars][::-1]
        line = chunk[chunk.find(' ') + 1:][::-1]
        text_to_wrap = text_to_wrap.replace(line+' ', '')
        lines.append(line)

    lines.append(text_to_wrap)
    return lines


class Recognition:
    def __init__(self):
        self.previous_line = ''
        self.chunk_queue = []
        self.next_chunk_id = 0

    def recognition_loop(self):
        while True:
            # Assign chunks
            chunk_id = self.next_chunk_id
            self.next_chunk_id += 1

            audio = self.listen()

            if audio is not None:
                self.chunk_queue.append(chunk_id)
                recognition_thread = threading.Thread(target=self.analyse_and_save, args=(audio, chunk_id))
                recognition_thread.start()

    def analyse_and_save(self, audio, chunk_id):

        # Perform speech recognition
        try:
            new_line = r.recognize_google(audio, language='pl-PL')

        except sr.UnknownValueError:
            clear_output()
            self.previous_line = ''

        except sr.RequestError as e:
            with open('recognition/output.txt', 'w', encoding='UTF-8') as f:
                f.write('Wystąpił błąd.')

        else:

            # Ensure chunks are in the right order
            while chunk_id != min(self.chunk_queue):
                time.sleep(0.2)

            # Process and save output
            lines = wrapping(self.previous_line + new_line)
            new_text = '\n'.join(lines[:2])
            self.previous_line = lines[-1] + ' '
            with open('recognition/output.txt', 'w', encoding='UTF-8') as f:
                f.write(new_text)

            self.chunk_queue.remove(chunk_id)

    def listen(self):
        try:
            with sr.Microphone(device_index=1) as source:
                return r.listen(source, phrase_time_limit=10, timeout=12)
        except sr.WaitTimeoutError:
            clear_output()
            return None
