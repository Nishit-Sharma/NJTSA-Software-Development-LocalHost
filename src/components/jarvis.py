# IF FFMPEG CRASHES, YOU NEED TO PUT IT INTO YOUR PYTHON SCRIPTS DIRECTORY: C:\Users\ZyptaR\AppData\Local\Programs\Python\Python39\Scripts

from elevenlabs.client import ElevenLabs
from elevenlabs import play, stream, save
import speech_recognition as sr
import webbrowser
import datetime
import json
import sys
import requests
import calendar
import os
import pyaudio
import ffmpeg
import calendar

class CalendarEvent:
    def __init__(self, name, datetime_obj):
        self.name = name
        self.datetime = datetime_obj

class Calendar:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event):
        self.events.remove(event)

    def get_events(self, date=None):
        if date:
            return [event for event in self.events if event.datetime.date() == date]
        else:
            return self.events

    def print_calendar(self):
        for event in self.events:
            print(f"{event.datetime.strftime('%Y-%m-%d %H:%M')} - {event.name}")
            
calendar = Calendar()

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
client = ElevenLabs(
  api_key="44bd2fafea55e550c58548571fe9f64d"
)

# Set up wake-up keyword
wake_word = "Jarvis"

# Define function to convert text to speech
def speak(text):
    audio = client.generate(text=text, voice="James Fitzgerald", model="eleven_multilingual_v2")
    play(audio)

# Define function for opening a website
def open_website(url):
    webbrowser.open(url)
    speak("Opening website.")

# Define function for telling the time
def tell_time():
    time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {time}.")

# Define function to add an event to the calendar
def add_calendar_event(r):
    with sr.Microphone(device_index=device_id['device_index']) as source:
        speak("What is the name of the event?")
        event_name = r.recognize_google(r.listen(source))
        print(f"You said: {event_name}")

        speak("What is the date of the event?") # Format Month, Day, Year is applicable
        event_date_str = r.recognize_google(r.listen(source))
        print(f"You said: {event_date_str}")

        # Split the date string into month, day, and year
        event_date_parts = event_date_str.split(" ")

        # Check if the date string has at least month and day
        if len(event_date_parts) < 1 or len(event_date_parts) > 3:
            speak("I'm sorry, I didn't understand the date format. Please try again.")
            return

        event_month_str = event_date_parts[0].strip()
        event_day_str = event_date_parts[1].strip()

        # Check if the year was provided
        if len(event_date_parts) > 2:
            event_year = int(event_date_parts[2].strip())
        else:
            event_year = datetime.date.today().year

        # Remove the day suffix (st, nd, rd, or th)
        event_day_str = event_day_str.rstrip("stndrdth")
        event_day = int(event_day_str)

        # Convert the month name to the corresponding number
        event_month = None
        for i, month_name in enumerate(calendar.month_name):
            if month_name.lower() == event_month_str.lower():
                event_month = i
                break
        if event_month is None:
            speak("I'm sorry, I didn't recognize that month name.")
            return
        
        speak("What is the time of the event?") # Format HH:MM AM/PM
        event_time_str = r.recognize_google(r.listen(source))
        print(f"You said: {event_time_str}")

        # Parse the event time string
        event_time_parts = event_time_str.split()
        event_time = event_time_parts[0]
        event_time_period = event_time_parts[1].upper()

        # Convert the time to 24-hour format
        event_time_parts = event_time.split(":")
        event_hour = int(event_time_parts[0])
        event_minute = int(event_time_parts[1])
        if event_time_period == "PM" and event_hour != 12:
            event_hour += 12
        elif event_time_period == "AM" and event_hour == 12:
            event_hour = 0

        # Create the event datetime object
        event_datetime = datetime.datetime(event_year, event_month, event_day, event_hour, event_minute)

        # Add the event to the calendar
        event = CalendarEvent(event_name, event_datetime)
        calendar.add_event(event)
        speak(f"Added the event '{event_name}' to your calendar.")

def set_reminder(r):
    with sr.Microphone(device_index=device_id['device_index']) as source:
        speak("What is the reminder text?")
        reminder_text = r.recognize_google(r.listen(source))
        print(f"You said: {reminder_text}")

        speak("What time would you like to set the reminder?") # Format Hour:Minute
        reminder_time = r.recognize_google(r.listen(source))
        print(f"You said: {reminder_time}")

        # Convert the reminder time to a datetime object
        reminder_datetime = datetime.datetime.strptime(reminder_time, "%H:%M")

        # Set the reminder
        # calendar.setreminder(reminder_text, reminder_datetime) # This is a placeholder function
        speak(f"I've set a reminder for '{reminder_text}' at {reminder_time}.")

# Define function to check the command and execute the appropriate action
def check_command(command, r):
    if "open" in command.lower():
        url = "https://www." + command.lower().split()[-1] + ".com"
        open_website(url)
    elif "time" in command.lower():
        tell_time()
    elif "weather" in command.lower():
        city = command.lower().split()[-1]
        weather_info = get_weather(city)
        speak(weather_info)
    elif "add" in command.lower() and "event" in command.lower():
        add_calendar_event(r)
    elif "set" in command.lower() and "reminder" in command.lower():
        set_reminder(r)
    elif "google" in command.lower():
        query = command.lower().replace("google", "").strip()
        if query:
            query = query.replace(" ", "+")
            url = f"https://www.google.com/search?q={query}"
            open_website(url)
        else:
            speak("What would you like me to search for on Google?")
    else:
        speak("I'm sorry, I didn't understand that.")

# Define function to get the weather information
def get_weather(city):
    api_key = "39c53008af40643aa03b01b0e27de931"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city + "&units=imperial"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"The weather in {city} is {weather} with a temperature of {temperature}°F."
    else:
        return f"Sorry, I couldn't find the weather information for {city}."

# Check if wake-up keyword is detected
speak("Hello Sir")

try:
    # Convert speech to text
    command = r.recognize_google(audio)
    print("You said: " + command)
    
    check_command(command, r)

except sr.UnknownValueError:
    speak("I'm sorry, I didn't understand that.")
except sr.RequestError as e:
    speak("Sorry, I couldn't reach the Google servers. Check your internet connection.")
    speak("Sorry, I couldn't reach the Google servers. Check your internet connection.")