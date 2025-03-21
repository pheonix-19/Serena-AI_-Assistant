import pyttsx3
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import threading

class TextToSpeech:
    def __init__(self, rate=150, volume=1.0, use_indian_english=True):
        self.use_gtts = True
        self.use_indian_english = use_indian_english
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        voices = self.engine.getProperty('voices')
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        self.speak_lock = threading.Lock()
        language = "Indian English" if use_indian_english else "Hindi"
        print(f"Text-to-speech initialized using {language}")

    def speak(self, text):
        if not text:
            return
        threading.Thread(target=self._speak_threaded, args=(text,)).start()

    def _speak_threaded(self, text):
        with self.speak_lock:
            try:
                if self.use_gtts:
                    self._speak_gtts(text)
                else:
                    self._speak_pyttsx3(text)
            except Exception as e:
                print(f"Error with gTTS: {e}. Falling back to pyttsx3.")
                self._speak_pyttsx3(text)

    def _speak_gtts(self, text):
        if self.use_indian_english:
            lang = "en"
            tld = "in"
        else:
            lang = "hi"
            tld = "com"
        mp3_fp = BytesIO()
        tts = gTTS(text=text, lang=lang, tld=tld)
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio = AudioSegment.from_mp3(mp3_fp)
        play(audio)

    def _speak_pyttsx3(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def switch_to_hindi(self):
        self.use_indian_english = False
        print("Switched to Hindi")

    def switch_to_indian_english(self):
        self.use_indian_english = True
        print("Switched to Indian English")

    def use_pyttsx3(self):
        self.use_gtts = False
        print("Using local speech engine")

    def use_google_tts(self):
        self.use_gtts = True
        print("Using Google speech engine")