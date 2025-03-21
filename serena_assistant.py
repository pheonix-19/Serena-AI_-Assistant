import datetime
import os
import speech_recognition as sr
import subprocess
import webbrowser
import time
import keyboard
import platform
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import json
from openai import OpenAI
import random
from PIL import Image, ImageTk, ImageSequence
from utils import TextToSpeech

class SerenaAssistant:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_voice()
        self.setup_recognizer()
        self.setup_openai()
        self.setup_personality()
        self.create_gui()

    def setup_window(self):
        self.root.title("Serena - AI Assistant")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        style = ttk.Style()
        style.configure('Custom.TFrame', background='#f0f0f0')
        style.configure('Custom.TButton', padding=10, font=('Arial', 10))
        style.configure('Status.TLabel', font=('Arial', 12))

    def setup_voice(self):
        self.tts = TextToSpeech(rate=120, volume=0.9, use_indian_english=True)

    def setup_recognizer(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 3000
        self.recognizer.pause_threshold = 0.8
        self.listening = False
        self.listen_thread = None

    def setup_openai(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            self.log_message("Warning: OPENAI_API_KEY not found in environment variables")
            return
        self.client = OpenAI(api_key=api_key)

    def setup_personality(self):
        self.greetings = [
            "  Hello! I'm Serena, your personal Assistant, What can I do for you?"
        ]
        self.acknowledgments = [
            "Right away!"
        ]
        self.error_responses = [
            "I didn't quite catch that. Could you please repeat?",
            "Sorry, I'm having trouble understanding. Can you try again?",
            "I missed that. One more time, please?",
            "Could you rephrase that for me?"
        ]

    def create_gui(self):
        self.main_frame = ttk.Frame(self.root, style='Custom.TFrame', padding="20")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            self.main_frame, 
            textvariable=self.status_var,
            style='Status.TLabel'
        )
        self.status_label.grid(row=0, column=0, pady=(0, 10), sticky="ew")
        self.history_frame = ttk.Frame(self.main_frame)
        self.history_frame.grid(row=1, column=0, sticky="nsew")
        self.history_frame.grid_columnconfigure(0, weight=1)
        self.history_frame.grid_rowconfigure(0, weight=1)
        self.history_text = scrolledtext.ScrolledText(
            self.history_frame,
            wrap=tk.WORD,
            font=('Arial', 10)
        )
        self.history_text.grid(row=0, column=0, sticky="nsew")
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=2, column=0, pady=(10, 0), sticky="ew")
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.start_button = ttk.Button(
            self.button_frame,
            text="Start Listening",
            command=self.toggle_listening,
            style='Custom.TButton'
        )
        self.start_button.grid(row=0, column=1)
        self.gif_label = tk.Label(self.main_frame)
        self.gif_label.grid(row=3, column=0, pady=10)
        self.gif_path = "gif/3.gif"
        self.gif = Image.open(self.gif_path)
        self.gif_frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(self.gif)]
        self.gif_index = 0
        self.animate_gif()
        self.greet()

    def animate_gif(self):
        frame = self.gif_frames[self.gif_index]
        self.gif_label.config(image=frame)
        self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
        self.root.after(100, self.animate_gif)

    def greet(self):
        greeting = random.choice(self.greetings)
        self.log_message(f"Serena: {greeting}")
        self.say(greeting)

    def toggle_listening(self):
        if not self.listening:
            self.start_listening()
        else:
            self.stop_listening()

    def start_listening(self):
        self.listening = True
        self.start_button.config(text="Stop Listening")
        self.status_var.set("Listening...")
        self.listen_thread = threading.Thread(target=self.listen_loop)
        self.listen_thread.daemon = True
        self.listen_thread.start()
        self.say(random.choice(self.acknowledgments))

    def stop_listening(self):
        self.listening = False
        self.start_button.config(text="Start Listening")
        self.status_var.set("Ready")
        if self.listen_thread:
            self.listen_thread.join(timeout=1)
        self.say("Listening stopped. Let me know if you need anything else!")

    def listen_loop(self):
        while self.listening:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    self.log_message("Listening...")
                    try:
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        command = self.recognizer.recognize_google(audio).lower()
                        if command:
                            self.log_message(f"You: {command}")
                            self.process_command(command)
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        self.log_message(random.choice(self.error_responses))
                    except Exception as e:
                        self.log_message(f"Error: {str(e)}")
            except Exception as e:
                self.log_message(f"Listening error: {str(e)}")
                time.sleep(1)

    def process_command(self, command):
        try:
            if any(phrase in command.lower() for phrase in ["switch to hindi", "speak in hindi", "use hindi"]):
                self.tts.switch_to_hindi()
                self.say("अब मैं हिंदी में बोलूंगी")
                return
            if any(phrase in command.lower() for phrase in ["switch to english", "speak in english", "use english", "use indian english"]):
                self.tts.switch_to_indian_english()
                self.say("Now I'll speak in Indian English")
                return
            if any(phrase in command.lower() for phrase in ["use local voice", "use windows voice"]):
                self.tts.use_pyttsx3()
                self.say("Using local voice engine")
                return
            if any(phrase in command.lower() for phrase in ["use google voice", "use online voice"]):
                self.tts.use_google_tts()
                self.say("Using Google Text to Speech")
                return
            if any(word in command for word in ['hey serena', 'hi serena', 'okay serena']):
                self.say(random.choice(self.acknowledgments))
                return
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Serena, a helpful female seductive voice assistant. Analyze the command and respond with a JSON object containing: category (web_search/system_control/application/media_control/voice_typing/information), action, and parameters."},
                    {"role": "user", "content": command}
                ]
            )
            result = json.loads(response.choices[0].message.content)
            category = result.get('category')
            parameters = result.get('parameters', {})
            if category == 'web_search':
                self.web_search(command)
            elif category == 'system_control':
                self.system_control(command)
            elif category == 'application':
                self.open_application(parameters.get('app_name', ''))
            elif category == 'media_control':
                self.media_control(command)
            elif category == 'voice_typing':
                self.voice_typing()
            elif category == 'information':
                self.get_information(command)
            else:
                self.say("I'm not sure how to help with that. Could you try rephrasing?")
        except Exception as e:
            self.log_message(f"Command processing error: {str(e)}")
            self.say("I encountered an error processing that command. Please try again.")

    def web_search(self, query):
        search_terms = query.replace('search', '').replace('google', '').strip()
        self.say(f"Searching for {search_terms}")
        webbrowser.open(f"https://www.google.com/search?q={search_terms}")

    def system_control(self, command):
        if 'shutdown' in command:
            self.say("Preparing to shut down the computer...")
            os.system('shutdown /s /t 60' if platform.system() == "Windows" else 'shutdown -h +1')
        elif 'restart' in command:
            self.say("Preparing to restart the computer...")
            os.system('shutdown /r /t 60' if platform.system() == "Windows" else 'shutdown -r +1')
        elif 'cancel shutdown' in command:
            self.say("Canceling shutdown...")
            os.system('shutdown /a' if platform.system() == "Windows" else 'shutdown -c')

    def open_application(self, app_name):
        try:
            if platform.system() == "Windows":
                os.startfile(app_name)
            else:
                subprocess.Popen([app_name])
            self.say(f"Opening {app_name}")
        except Exception as e:
            self.say(f"Sorry, I couldn't open {app_name}")

    def media_control(self, command):
        if 'play' in command or 'pause' in command:
            keyboard.press_and_release('play/pause media')
        elif 'next' in command:
            keyboard.press_and_release('next track')
        elif 'previous' in command:
            keyboard.press_and_release('previous track')

    def voice_typing(self):
        self.say("Voice typing mode enabled. Speak your text.")
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=10)
                text = self.recognizer.recognize_google(audio)
                keyboard.write(text)
                self.say("Text typed successfully")
        except Exception as e:
            self.say("Sorry, I couldn't type that.")

    def get_information(self, query):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Serena, a female personal friendly and interactive AI assistant. Respond to the following user input in a conversational and engaging manner. Provide comprehensive and very short but concise information about the query."},
                    {"role": "user", "content": query}
                ]
            )
            answer = response.choices[0].message.content
            self.say(answer)
        except Exception as e:
            self.say("I'm sorry, I couldn't find that information.")

    def log_message(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.history_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.history_text.see(tk.END)

    def say(self, text):
        self.log_message(f"Serena: {text}")
        self.tts.speak(text)