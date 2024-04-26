import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import json
import sys
import pyaudio
import os

# Get the stream data from the command-line argument
try:
    device_id = json.loads(sys.argv[1])
except (IndexError, json.JSONDecodeError) as e:
    print(f"Error decoding JSON: {e}")
    # Handle the error, e.g., exit the script or provide a default value
    device_id = {'device_index': 0}

# Create a speech recognition instance and set the audio source
r = sr.Recognizer()

# List available microphones
# print("Available microphones:")
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f"{index}: {name}")

# Select the microphone
with sr.Microphone(device_index=device_id['device_index']) as source:
    print("Listening...")
    r.pause_threshold = 1
    audio = r.listen(source)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set up wake-up keyword
wake_word = "Jarvis"

# Define function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define function for opening a website
def open_website(url):
    webbrowser.open(url)
    speak("Opening website.")

# Define function for telling the time
def tell_time():
    time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {time}.")

# Check if wake-up keyword is detected
speak("Hello Sir")

try:
    # Convert speech to text
    command = r.recognize_google(audio)
    print("You said: " + command)
    
    # Execute command
    if "open" in command:
        if "website" in command:
            url = "https://www." + command.split()[-1] + ".com"
            open_website(url)
        else:
            speak("I'm not sure what you want me to open.")
    elif "time" in command:
        tell_time()
    else:
        speak("I'm sorry, I didn't understand that.")

except sr.UnknownValueError:
    speak("I'm sorry, I didn't understand that.")
except sr.RequestError as e:
    speak("Sorry, I couldn't reach the Google servers. Check your internet connection.")