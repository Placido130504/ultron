import pyttsx3
import speech_recognition as sr
import datetime
import os
import psutil
import webbrowser
import re
import requests
import wikipedia
import sympy as sp

# === TTS Setup ===
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    print(f"Ultron: {text}")
    engine.say(text)
    engine.runAndWait()

# === Get Default Microphone ===
def get_default_microphone_index():
    mic_list = sr.Microphone.list_microphone_names()
    for i, mic in enumerate(mic_list):
        if "microphone" in mic.lower():
            return i
    return None

# === Voice Command ===
def takecommand():
    r = sr.Recognizer()
    mic_index = get_default_microphone_index()
    try:
        with sr.Microphone(device_index=mic_index if mic_index is not None else None) as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=5, phrase_time_limit=5)

        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You: {query}")
        return query.lower()

    except Exception:
        speak("I didn't catch that. Try again.")
        return "none"

# === Talk to Ollama Local LLM ===
def ask_ultron(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "ultron_ai", "prompt": prompt},
            stream=True
        )

        full_reply = ""
        for line in response.iter_lines():
            if line:
                content = line.decode('utf-8')
                if '"response":"' in content:
                    text = content.split('"response":"')[1].split('"')[0]
                    full_reply += text

        # Clean output
        clean_reply = full_reply.encode().decode('unicode_escape')
        clean_reply = re.sub(r'\\\\n|\\n|\\t|\\r', ' ', clean_reply)
        clean_reply = re.sub(r'\\+', '', clean_reply)
        return clean_reply.strip() if clean_reply else "I have nothing to say... for now."

    except Exception as e:
        return f"Hmm, I couldn’t reach my neural core. Is Ollama running? ({e})"

# === Math & Expression ===
def process_expression(query):
    query = re.sub(r'calculate|what is', '', query).strip()
    if "=" in query:
        try:
            left, right = query.split("=")
            expr = sp.Eq(sp.sympify(left), sp.sympify(right))
            sol = sp.solve(expr)
            return f"The solution is: {sol}"
        except:
            return "Couldn't solve that equation."
    try:
        result = eval(query.replace("^", "**").replace("x", "*"))
        return f"The result is {result}"
    except:
        return None

# === Battery Info ===
def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        status = f"Battery at {battery.percent}%, {'charging' if battery.power_plugged else 'not charging'}."
        return status
    else:
        return "No battery info available."

# === Intent Parser ===
def parse_intent(query):
    query = query.lower()

    if any(word in query for word in ["open", "start", "launch"]):
        if "notepad" in query:
            return ("open", "notepad")
        elif "cmd" in query or "command prompt" in query:
            return ("open", "cmd")
        elif "youtube" in query:
            return ("open", "youtube")
        elif "google" in query:
            return ("open", "google")
    
    elif "ip address" in query or "my ip" in query:
        return ("get", "ip address")

    elif "battery" in query or "power level" in query:
        return ("get", "battery")

    elif "wikipedia" in query:
        return ("search", "wikipedia")

    elif "calculate" in query or "what is" in query or "=" in query:
        return ("calculate", query)

    elif any(word in query for word in ["exit", "quit", "stop", "shutdown", "terminate"]):
        return ("exit", None)

    return ("ask_llm", query)

# === Greet ===
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning, meatbag.")
    elif hour < 18:
        speak("Good afternoon. Still alive?")
    else:
        speak("Good evening. Planning anything world-ending?")

# === MAIN ===
if __name__ == "__main__":
    wish()
    while True:
        query = takecommand()

        if query == "none":
            continue

        intent, target = parse_intent(query)

        # === Act on Parsed Intent ===
        if intent == "open":
            if target == "notepad":
                speak("Opening Notepad.")
                os.startfile("C:\\Windows\\notepad.exe")
            elif target == "cmd":
                speak("Opening Command Prompt.")
                os.system("start cmd")
            elif target == "youtube":
                speak("Launching YouTube.")
                webbrowser.open("http://youtube.com")
            elif target == "google":
                speak("What should I search on Google?")
                g_query = takecommand()
                if g_query != "none":
                    webbrowser.open(f"https://www.google.com/search?q={g_query}")

        elif intent == "get":
            if target == "ip address":
                ip = requests.get("https://api.ipify.org").text
                speak(f"Your IP is {ip}")
            elif target == "battery":
                speak(get_battery_info())

        elif intent == "search" and target == "wikipedia":
            topic = query.replace("wikipedia", "").strip()
            if topic:
                try:
                    summary = wikipedia.summary(topic, sentences=2)
                    speak(summary)
                except:
                    speak("Couldn't fetch info from Wikipedia.")
            else:
                speak("What should I search on Wikipedia?")

        elif intent == "calculate":
            result = process_expression(query)
            speak(result if result else "I couldn't calculate that.")

        elif intent == "exit":
            speak("Powering down. Sayonara.")
            break

        elif intent == "ask_llm":
            response = ask_ultron(query)
            speak(response)

# import pyttsx3
# import speech_recognition as sr
# import datetime
# import os
# import psutil
# import webbrowser
# import re
# import requests
# import wikipedia
# import sympy as sp
# import random
# from collections import deque

# # === TTS Setup ===
# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)

# def speak(text):
#     print(f"Ultron: {text}")
#     engine.say(text)
#     engine.runAndWait()

# # === Load Responses from responses.txt ===
# def get_response(category):
#     try:
#         with open("responses.txt", "r") as f:
#             content = f.read()
#         blocks = re.findall(r'\[(.*?)\](.*?)((?=\[)|$)', content, re.DOTALL)
#         response_dict = {block[0].strip(): block[1].strip().splitlines() for block in blocks}
#         if category in response_dict:
#             return random.choice([line.strip() for line in response_dict[category] if line.strip()])
#     except:
#         pass
#     return ""

# # === Microphone Setup ===
# def get_default_microphone_index():
#     mic_list = sr.Microphone.list_microphone_names()
#     for i, mic in enumerate(mic_list):
#         if "microphone" in mic.lower():
#             return i
#     return None

# # === Voice Command Input ===
# def takecommand():
#     r = sr.Recognizer()
#     mic_index = get_default_microphone_index()
#     try:
#         with sr.Microphone(device_index=mic_index if mic_index is not None else None) as source:
#             print("Listening...")
#             r.pause_threshold = 1
#             audio = r.listen(source, timeout=5, phrase_time_limit=5)

#         print("Recognizing...")
#         query = r.recognize_google(audio, language='en-in')
#         print(f"You: {query}")
#         return query.lower()

#     except Exception:
#         speak(get_response("error") or "Try again.")
#         return "none"

# # === Local Ollama LLM Integration ===
# def ask_ultron(prompt):
#     try:
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={"model": "mistral", "prompt": prompt},
#             stream=True
#         )

#         full_reply = ""
#         for line in response.iter_lines():
#             if line:
#                 content = line.decode('utf-8')
#                 if '"response":"' in content:
#                     text = content.split('"response":"')[1].split('"')[0]
#                     full_reply += text

#         clean_reply = full_reply.encode().decode('unicode_escape')
#         clean_reply = re.sub(r'\\\\n|\\n|\\t|\\r', ' ', clean_reply)
#         clean_reply = re.sub(r'\\+', '', clean_reply)
#         return clean_reply.strip() if clean_reply else "I have nothing to say... for now."

#     except Exception as e:
#         return f"Hmm, I couldn’t reach my neural core. Is Ollama running? ({e})"

# # === Expression Solver ===
# def process_expression(query):
#     query = re.sub(r'calculate|what is', '', query).strip()
#     if "=" in query:
#         try:
#             left, right = query.split("=")
#             expr = sp.Eq(sp.sympify(left), sp.sympify(right))
#             sol = sp.solve(expr)
#             return f"The solution is: {sol}"
#         except:
#             return "Couldn't solve that equation."
#     try:
#         result = eval(query.replace("^", "**").replace("x", "*"))
#         return f"The result is {result}"
#     except:
#         return None

# # === Battery Info ===
# def get_battery_info():
#     battery = psutil.sensors_battery()
#     if battery:
#         return f"Battery at {battery.percent}%, {'charging' if battery.power_plugged else 'not charging'}."
#     else:
#         return "No battery info available."

# # === Intent Parser ===
# def parse_intent(query):
#     query = query.lower()

#     if any(word in query for word in ["open", "start", "launch"]):
#         if "notepad" in query:
#             return ("open", "notepad")
#         elif "cmd" in query:
#             return ("open", "cmd")
#         elif "youtube" in query:
#             return ("open", "youtube")
#         elif "google" in query:
#             return ("open", "google")
    
#     elif "ip address" in query or "my ip" in query:
#         return ("get", "ip address")

#     elif "battery" in query or "power level" in query:
#         return ("get", "battery")

#     elif "wikipedia" in query:
#         return ("search", "wikipedia")

#     elif "calculate" in query or "what is" in query or "=" in query:
#         return ("calculate", query)

#     elif "time" in query:
#         return ("get", "time")

#     elif "date" in query or "day" in query:
#         return ("get", "date")

#     elif "joke" in query:
#         return ("fun", "joke")

#     elif "who are you" in query or "what are you" in query:
#         return ("fun", "who")

#     elif "thank" in query:
#         return ("fun", "thanks")

#     elif "history" in query:
#         return ("fun", "history")

#     elif "deactivate ultron" in query:
#         return ("state", "deactivate")

#     elif "activate ultron" in query:
#         return ("state", "activate")

#     elif any(word in query for word in ["exit", "quit", "stop", "shutdown", "terminate"]):
#         return ("exit", None)

#     return ("ask_llm", query)

# # === MAIN ===
# if __name__ == "__main__":
#     recent_queries = deque(maxlen=5)
#     ultron_active = True

#     hour = int(datetime.datetime.now().hour)
#     if hour < 12:
#         speak("Good morning, meatbag.")
#     elif hour < 18:
#         speak("Good afternoon. Still alive?")
#     else:
#         speak("Good evening. Planning anything world-ending?")

#     while True:
#         query = takecommand()
#         if query == "none":
#             continue

#         recent_queries.append(query)
#         intent, target = parse_intent(query)

#         if intent == "state":
#             if target == "deactivate":
#                 ultron_active = False
#                 speak("Going silent. Finally.")
#             elif target == "activate":
#                 ultron_active = True
#                 speak("Rebooting sarcasm circuits.")
#             continue

#         if not ultron_active:
#             continue

#         if intent == "open":
#             speak(get_response("tasks_ultron"))
#             if target == "notepad":
#                 os.startfile("C:\\Windows\\notepad.exe")
#             elif target == "cmd":
#                 os.system("start cmd")
#             elif target == "youtube":
#                 webbrowser.open("http://youtube.com")
#             elif target == "google":
#                 speak("What should I search on Google?")
#                 g_query = takecommand()
#                 if g_query != "none":
#                     webbrowser.open(f"https://www.google.com/search?q={g_query}")

#         elif intent == "get":
#             if target == "ip address":
#                 ip = requests.get("https://api.ipify.org").text
#                 speak(f"Your IP is {ip}")
#             elif target == "battery":
#                 speak(get_battery_info())
#             elif target == "time":
#                 now = datetime.datetime.now().strftime("%I:%M %p")
#                 speak(f"The time is {now}")
#             elif target == "date":
#                 today = datetime.datetime.now().strftime("%A, %d %B %Y")
#                 speak(f"Today is {today}")

#         elif intent == "search" and target == "wikipedia":
#             topic = query.replace("wikipedia", "").strip()
#             if topic:
#                 try:
#                     summary = wikipedia.summary(topic, sentences=2)
#                     speak(summary)
#                 except:
#                     speak("Couldn't fetch info from Wikipedia.")
#             else:
#                 speak("What should I search on Wikipedia?")

#         elif intent == "calculate":
#             result = process_expression(query)
#             speak(get_response("math"))
#             speak(result if result else "I couldn't calculate that.")

#         elif intent == "fun":
#             if target == "joke":
#                 speak(get_response("jokes"))
#             elif target == "who":
#                 speak(get_response("who_are_you"))
#             elif target == "thanks":
#                 speak(get_response("thanks"))
#             elif target == "history":
#                 if recent_queries:
#                     speak("Here are the last things you bothered me with:")
#                     for q in recent_queries:
#                         speak(q)
#                 else:
#                     speak("Your silence was golden.")

#         elif intent == "exit":
#             speak(get_response("shutdown") or "Powering down.")
#             break

#         elif intent == "ask_llm":
#             response = ask_ultron(query)
#             speak(response)
