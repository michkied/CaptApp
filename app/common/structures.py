import json
from dataclasses import dataclass


@dataclass
class AppSettings:
    font_size: int = 16
    transparency_value: int = 175
    interface_lang: str = 'en'
    audio_lang: str = 'en'
    overlay_width: int = 0
    overlay_height: int = 0
    save_caption_to_file: bool = False
    display_welcome_message: bool = True

    def __init__(self):
        try:
            with open('app/gui/settings.json', 'r', encoding='UTF-8') as f:
                settings = json.loads(f.read())
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            settings = {
                'fontSize': self.font_size,
                'transparencyValue': self.transparency_value,
                'interfaceLang': self.interface_lang,
                'audioLang': self.audio_lang,
                'overlayWidth': self.overlay_width,
                'overlayHeight': self.overlay_height,
                'saveCaption': self.save_caption_to_file,
                'displayWelcomeMessage': self.display_welcome_message
            }
            with open('app/gui/settings.json', 'w', encoding='UTF-8') as f:
                f.write(json.dumps(settings))

        self.font_size = settings['fontSize']
        self.transparency_value = settings['transparencyValue']
        self.interface_lang = settings['interfaceLang']
        self.audio_lang = settings['audioLang']
        self.overlay_width = settings['overlayWidth']
        self.overlay_height = settings['overlayHeight']
        self.save_caption_to_file = settings['saveCaption']
        self.display_welcome_message = settings['displayWelcomeMessage']

    def save_to_file(self):
        data = {
            'fontSize': self.font_size,
            'transparencyValue': self.transparency_value,
            'interfaceLang': self.interface_lang,
            'audioLang': self.audio_lang,
            'overlayWidth': self.overlay_width,
            'overlayHeight': self.overlay_height,
            'saveCaption': self.save_caption_to_file,
            'displayWelcomeMessage': self.display_welcome_message
        }

        with open('app/gui/settings.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(data, indent=4))
