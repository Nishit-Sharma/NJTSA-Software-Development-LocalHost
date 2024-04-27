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
from g4f.client import Client
import re
import io
import wolframalpha

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
wake_word = "Apollo"

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
        if len(event_date_parts) < 2 or len(event_date_parts) > 3:
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
        month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        event_month = next((i for i, month in enumerate(month_names) if month.lower() == event_month_str.lower()), None)
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
        event_datetime = datetime.datetime(event_year, event_month + 1, event_day, event_hour, event_minute)

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


def gpt_math(
    inputtext="what is ten times 9 plus fifty five to the power of 7 and then all of that square rooted",
):
    _client = Client()
    
    response = _client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"""I will give you a math expression and you give me a python code that will calculate it and then print it out

    {inputtext}""",
            }
        ],
    )

    response = response.choices[0].message.content.replace("```python", "```")

    matches = re.findall(r"(?<=```).*?(?=```)", response, re.DOTALL)

    response = matches[0]

    print(response)
    
    try:
        # Temporarily set output into a string variable
        output = io.StringIO()
        sys.stdout = output
        
        exec(response)
        
        # Revert
        output_str = output.getvalue()
        sys.stdout = sys.__stdout__
        
        print(output_str)
        speak(output_str)
    except:
        speak("I'm sorry, I couldn't calculate that expression.")
        

def ask_gpt(
    inputtext="hi!",
):
    _client = Client()
    
    response = _client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"""Respond to the following user prompt in a sentence or two, your name is "Apollo":
    
{inputtext}            
""",
            }
        ],
    )

    response = response.choices[0].message.content
    
    try:
        print(response)
        speak(response)
    except:
        speak("I'm sorry, can you say that again?")
        
def ask_wolframalpha(question, app_id = "TYJYRK-UVWT679K48"):
    """
    Queries WolframAlpha with the given question and returns the response text.

    Parameters:
    - question (str): The question to ask WolframAlpha.
    - app_id (str): The app ID obtained from WolframAlpha.
    """
    
    _client = Client()
    
    response = _client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"""Turn the following user inputted question for Wolfram Alpha into an input string that Wolfram Alpha can understand. Only respond with the input string. Surround your response with two $ symbols like &&this&&.
    
{question}            
""",
            }
        ],
    )

    response = response.choices[0].message.content
    # Regex pattern to match everything between "&&"
    pattern = r'\&\&(.*?)\&\&'
    # Find all matches
    matches = re.findall(pattern, response)

    try:
        response = matches[0]
        
        # Instance of WolframAlpha client class
        client = wolframalpha.Client(app_id)

        # Stores the response from WolframAlpha
        res = client.query(question)

        # Includes only text from the response
        answer = next(res.results).text

        speak(answer)
    except:
        speak("I'm sorry, I didn't understand that.")


# Define function to check the command and execute the appropriate action
def check_command(command, r):
    # OPEN WORKS
    if "open" in command.lower():
        url = "https://www." + command.lower().split()[-1] + ".com"
        open_website(url)
    # TIME WORKS
    elif "time" in command.lower():
        tell_time()
    # WEATHER WORKS
    elif "weather" in command.lower():
        city = command.lower().split()[-1]
        weather_info = get_weather(city)
        speak(weather_info)
    # ALL CALENDAR STUFF WORKS
    elif "add" in command.lower() and "event" in command.lower():
        add_calendar_event(r)
    elif "set" in command.lower() and "reminder" in command.lower():
        set_reminder(r)
    # GOOGLE SEARCH WORKS
    elif "google" in command.lower():
        query = command.lower().replace("google", "").strip()
        if query:
            query = query.replace(" ", "+")
            url = f"https://www.google.com/search?q={query}"
            open_website(url)
        else:
            speak("What would you like me to search for on Google?")
    # MATH CALCULATION WORKS
    elif "calculate" in command.lower():
        gpt_math(command.lower().replace("calculate", "").strip())
    elif "wolfram" in command.lower():
        ask_wolframalpha(command.lower().strip())
    # GPT CHAT WORKS
    else:
        query = command.lower()
        if query:
            ask_gpt(query)
        else:
            speak("What would you like to chat about?")
# Check if wake-up keyword is detected
speak("Hello Sir")
try:
    # Create a speech recognition instance and set the audio source
    r = sr.Recognizer()
    with sr.Microphone(device_index=device_id['device_index']) as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    # Convert speech to text
    command = r.recognize_google(audio)
    print("You said: " + command)
        
    check_command(command, r)
        
    if "goodbye" in command.lower() or "exit" in command.lower():
        speak("Goodbye!")
    
except sr.UnknownValueError:
    speak("I'm sorry, I didn't understand that.")
except sr.RequestError as e:
    speak("Sorry, I couldn't reach the Google servers. Check your internet connection.")
