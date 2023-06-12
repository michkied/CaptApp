import time
import speech_recognition as sr
import threading

r = sr.Recognizer()
r.pause_threshold = 0.5


def get_wrapped_lines(text_to_wrap, overlay):
    # Get display data

    num_of_chars = round(overlay.width / (overlay.p.settings.font_size * 0.75))

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
    def __init__(self, overlay):
        self.overlay = overlay
        self.carry = ''
        self.chunk_queue = []
        self.next_chunk_id = 0

    def recognition_loop(self):
        while not self.overlay.p.is_toggle_run:
            chunk_id = self.next_chunk_id
            self.next_chunk_id += 1

            audio = self.listen()

            if audio is not None:
                self.chunk_queue.append(chunk_id)
                recognition_thread = threading.Thread(target=self.process_audio, args=(audio, chunk_id))
                recognition_thread.start()

    def process_audio(self, audio, chunk_id):
        language = self.overlay.p.settings.audio_lang

        # Perform speech recognition
        try:
            new_line = r.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            self.overlay.to_display = self.overlay.p.gt(self.overlay.welcome_text)
            self.carry = ''
        except sr.RequestError as e:
            self.overlay.to_display = self.overlay.p.gt(self.overlay.error_text)

        else:
            while chunk_id != min(self.chunk_queue):  # Ensure chunks are in the right order
                time.sleep(0.1)
            self.display(new_line)

        self.chunk_queue.remove(chunk_id)

    def display(self, new_line):
        lines = get_wrapped_lines(self.carry + new_line, self.overlay)
        new_text = '\n'.join(lines[:2])

        if len(lines) == 1:
            self.carry = lines[-1] + '\n'  # If there is only one line, keep it
        else:
            if len(lines) == 2:  # If there are two lines, don't keep them
                self.carry = ''
            else:
                self.carry = '\n'.join(lines[2:]) + ' '  # If there are more than 2 lines, display them next time

        self.overlay.to_display = new_text

        # Give time to read
        time.sleep(len(new_line) / 27)

    def listen(self):
        try:
            with sr.Speaker() as source:
                return r.listen(source, phrase_time_limit=5, timeout=12)

        except sr.WaitTimeoutError:

            # Wait until all is read
            while self.chunk_queue:
                time.sleep(0.5)
            self.overlay.to_display = self.overlay.p.gt(self.overlay.welcome_text)

            return None
