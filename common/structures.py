import json
from dataclasses import dataclass


@dataclass
class AppSettings:
    font_size: int = 16
    transparency_value: int = 175
    interface_lang: str = 'en'
    audio_lang: str = 'en'
    overlay_width: int = 2048
    overlay_height: int = 79

    def __init__(self):
        try:
            with open('gui/settings.json', 'r', encoding='UTF-8') as f:
                settings = json.loads(f.read())
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            settings = {
                'fontSize': self.font_size,
                'transparencyValue': self.transparency_value,
                'interfaceLang': self.interface_lang,
                'audioLang': self.audio_lang
            }
            with open('gui/settings.json', 'w', encoding='UTF-8') as f:
                f.write(json.dumps(settings))

        self.font_size = settings['fontSize']
        self.transparency_value = settings['transparencyValue']
        self.interface_lang = settings['interfaceLang']
        self.audio_lang = settings['audioLang']

    def save_to_file(self):
        data = {
            'fontSize': self.font_size,
            'transparencyValue': self.transparency_value,
            'interfaceLang': self.interface_lang,
            'audioLang': self.audio_lang,
            'overlayWidth': self.overlay_width,
            'overlayHeight': self.overlay_height
        }

        with open('gui/settings.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(data, indent=4))
