import pyttsx3

class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._setup_voice()

    def _setup_voice(self):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # Personalizar voz aquí

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
