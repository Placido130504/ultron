Ultron Voice AI Assistant
Ultron is a locally running, voice-controlled AI assistant powered by speech recognition, text-to-speech, and a large language model (LLM) via [Ollama](https://ollama.com). It understands your commands, performs local tasks, answers questions, solves math, and responds with an attitude.This project goes beyond just voice recognition and automation. A separate file (ultron_responses.txt) defines how Ultron talks — giving it a consistent tone and emotional flavor. Whether it’s a witty comeback, a dry acknowledgment, or a mock-glitch error, Ultron feels like it has opinions.
This isn’t required for functionality — but it makes interaction human. And that’s kind of the point.

Features include:

Voice Recognition using Google Speech Recognition (offline mic support)
Text-to-Speech feedback using `pyttsx3`
LLM Integration via local Ollama model (`ultron_ai`)
Natural Language Intent Parsing
Wikipedia Lookup
Math & Equation Solver (`sympy`, `eval`)
-Internet Commands (Google, YouTube)
System Tools (Notepad, CMD)
System Info (Battery %, IP Address)
Sarcastic Personality responses (Ultron-themed)
Voice Shutdown

Setup Instructions and Requirements:

Install these Python packages:
pip install pyttsx3 SpeechRecognition wikipedia psutil sympy requests

To run, use command 'python ultron_ai.py'

Ultron connects to a locally running Ollama instance:
POST http://localhost:11434/api/generate
[Make sure your Ollama model is named ultron_ai. You can customize your Modelfile for Ultron’s tone and behavior]

Example use case:
You: What is the square root of 81?
Ultron: The result is 9. Basic, but acceptable.

License
This project is licensed under the MIT License — meaning you’re free to use, modify, distribute, or build on top of it, personally or commercially. Just leave credit where it’s due.
No warranties. No strings attached. Just code.
