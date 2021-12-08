import time
import speech_recognition as sr
import json
import threading

r = sr.Recognizer()
r.pause_threshold = 0.5


def clear_output():
    with open('temp/output.txt', 'w', encoding='UTF-8') as f:
        f.write('###CLEAR###')


def get_wrapped_lines(text_to_wrap):
    # Get display data
    with open('temp/display_data.json', 'r', encoding='UTF-8') as f:
        data = json.loads(f.read())

    with open('gui/settings.json', 'r', encoding='UTF-8') as f:
        fontsize = json.loads(f.read())['fontSize']

    num_of_chars = round(data['width'] / (fontsize * 0.75))

    lines = []

    # Handle lines carried from last time
    if text_to_wrap.count('\n') > 0:
        ttw_lines = text_to_wrap.split('\n')
        for line in ttw_lines[:-1]:
            lines.append(line)
        text_to_wrap = ttw_lines[-1]

    while len(text_to_wrap) > num_of_chars:
        chunk = text_to_wrap[:num_of_chars][::-1]  # Limit the chunk to max number of chars and flip it
        line = chunk[chunk.find(' ') + 1:][::-1]  # Find the end of the line (first space of the flipped chunk), crop the string, flip it back
        text_to_wrap = text_to_wrap.replace(line+' ', '')  # Remove extracted line from the rest of the text
        lines.append(line)

    lines.append(text_to_wrap)
    return lines


class Recognition:
    def __init__(self):
        self.carry = ''
        self.chunk_queue = []
        self.next_chunk_id = 0

    def recognition_loop(self):
        while True:
            chunk_id = self.next_chunk_id
            self.next_chunk_id += 1

            audio = self.listen()

            if audio is not None:
                self.chunk_queue.append(chunk_id)
                recognition_thread = threading.Thread(target=self.process_audio, args=(audio, chunk_id))
                recognition_thread.start()

    def process_audio(self, audio, chunk_id):

        with open('gui/settings.json', 'r', encoding='UTF-8') as f:
            language = json.loads(f.read())['audioLang']

        # Perform speech recognition
        try:
            new_line = r.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            clear_output()
            self.carry = ''
        except sr.RequestError as e:
            with open('temp/output.txt', 'w', encoding='UTF-8') as f:
                f.write('###ERROR###')

        else:
            while chunk_id != min(self.chunk_queue):  # Ensure chunks are in the right order
                time.sleep(0.1)
            self.save(new_line)

        self.chunk_queue.remove(chunk_id)

    def save(self, new_line):
        lines = get_wrapped_lines(self.carry + new_line)
        new_text = '\n'.join(lines[:2])

        if len(lines) == 1:
            self.carry = lines[-1] + '\n'  # If there is only one line, keep it
        else:
            if len(lines) == 2:  # If there are two lines, don't keep them
                self.carry = ''
            else:
                self.carry = '\n'.join(lines[2:]) + ' '  # If there are more than 2 lines, display them next time

        with open('temp/output.txt', 'w', encoding='UTF-8') as f:
            f.write(new_text)

        # Give time to read
        time.sleep(len(new_line) / 27)

    def listen(self):
        try:
            with sr.Microphone(device_index=1) as source:
                return r.listen(source, phrase_time_limit=10, timeout=12)

        except sr.WaitTimeoutError:

            # Wait until all is read
            while self.chunk_queue:
                time.sleep(0.5)
            clear_output()

            return None
