import speech_recognition as sr

r = sr.Recognizer()
r.pause_threshold = 0.5

# print(sr.Microphone.list_microphone_names())


def recognise_loop():

    def clear_output():
        with open('recognition/output.txt', 'w+', encoding='UTF-8') as f:
            f.write('Słucham... (wciśnij ESC by zamknąć)')

    previous_line = ''

    while True:

        # Listen to audio
        try:
            with sr.Microphone(device_index=1) as source:
                audio = r.listen(source, phrase_time_limit=10, timeout=12)
        except sr.WaitTimeoutError:
            clear_output()
            previous_line = ''
            continue

        # Perform speech recognition
        try:
            new_line = r.recognize_google(audio, language='pl-PL')

        except sr.UnknownValueError:
            clear_output()
            previous_line = ''

        except sr.RequestError as e:
            with open('recognition/output.txt', 'w+', encoding='UTF-8') as f:
                f.write('Wystąpił błąd.')

        else:

            # Add line breaks if necessary
            if len(new_line) > 150:
                new_line = (new_line[::-1].replace(' ', '\n', 1))[::-1] + ' '
            else:
                new_line = new_line + '\n'

            with open('recognition/output.txt', 'w+', encoding='UTF-8') as f:
                f.write(previous_line + new_line)

            previous_line = new_line
