import speech_recognition as sr
import json

r = sr.Recognizer()
r.pause_threshold = 0.5

# print(sr.Microphone.list_microphone_names())


def clear_output():
    with open('recognition/output.txt', 'w+', encoding='UTF-8') as f:
        f.write('Słucham... (wciśnij ESC by zamknąć)')


def wrapping(text_to_wrap):
    # Get display data
    with open('gui/display_data.json', 'r+', encoding='UTF-8') as f:
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


def recognise_loop():
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

            lines = wrapping(previous_line + new_line)
            new_text = '\n'.join(lines[:2])
            previous_line = lines[-1] + ' '

            with open('recognition/output.txt', 'w+', encoding='UTF-8') as f:
                f.write(new_text)
