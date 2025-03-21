# Serena AI Assistant

Serena is a desktop-based voice-controlled AI assistant built with Python. It combines speech recognition, natural language processing, and text-to-speech technologies to create an interactive and helpful digital companion. With its animated interface and multilingual capabilities, Serena brings a personal touch to your digital experience.

![3](https://github.com/user-attachments/assets/c3bb2bdf-1bb9-433c-b9c3-7964a4a903a5)

# ✨ Key Features

- Voice-Controlled Interface: Interact naturally using voice commands
- Multilingual Support: Switch between English and Hindi
- Multiple TTS Engines: Choose between local (pyttsx3) or online (Google TTS) voice engines
- Animated Character: Visual feedback through an animated avatar
- Cross-Platform: Works on Windows, macOS, and Linux
- AI-Powered Responses: Uses OpenAI's GPT-3.5 for intelligent responses

![Screenshot 2025-03-20 214947](https://github.com/user-attachments/assets/66fc92c1-e22b-4630-b28d-caf1ddd4f878)
# 🧠 Capabilities
Serena can help with a variety of tasks:

- Web Search: "Search for weather in New York"
- System Control: "Shutdown my computer in 1 hour"
- Application Management: "Open Notepad"
- Media Controls: "Play music" or "Pause the song"
- Voice Typing: Type text using your voice
- Information Retrieval: "What is the capital of France?"
- Language Switching: "Switch to Hindi" or "Use English"

# 🛠️ Installation
Prerequisites

- Python 3.6 or higher
- OpenAI API key

# Setup

1. Clone the repository:
```
git clone https://github.com/yourusername/serena-assistant.git
cd serena-assistant
```
2. pip install -r requirements.txt
```
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```
   # On Windows
set OPENAI_API_KEY=your_api_key_here

# On macOS/Linux
export OPENAI_API_KEY=your_api_key_here
   ```

4. Run the application:
   ```
   python main.py
   ```
   
# 📋 Dependencies

- tkinter: GUI framework
- speech_recognition: Voice input processing
- pyttsx3 & gTTS: Text-to-speech engines
- openai: Natural language processing
- PIL: Animation handling
- pydub: Audio playback
- keyboard: System control

# 📁 Project Structure

```
serena-assistant/
│
├── main.py                 # Entry point
├── serena_assistant.py     # Core assistant functionality
├── utils.py                # Text-to-speech utilities
├── requirements.txt        # Package dependencies
├── README.md               # This documentation
│
├── gif/                    # Animation assets
│   └── 3.gif               # Animated character
│
└── assets/                 # Documentation assets
    └── serena-flowchart.png  # Process flow diagram
```

# 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

- Fork the repository
- Create your feature branch (git checkout -b feature/amazing-feature)
- Commit your changes (git commit -m 'Add some amazing feature')
- Push to the branch (git push origin feature/amazing-feature)
- Open a Pull Request


# 📧 Contact
For questions or feedback, please open an issue or contact ayush.official1901@gmail.com.
