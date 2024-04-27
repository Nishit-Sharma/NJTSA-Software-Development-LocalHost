# IF FFMPEG CRASHES, YOU NEED TO PUT IT INTO YOUR PYTHON SCRIPTS DIRECTORY: C:\Users\ZyptaR\AppData\Local\Programs\Python\Python39\Scripts

# Importing a whole lotta yap
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
    """
    Represents a single event in the calendar.
    """
    def __init__(self, name, datetime_obj):
        """
        Initializes a CalendarEvent object with the given name and datetime.
        
        Args:
            name (str): The name of the event.
            datetime_obj (datetime): The date and time of the event.
        """
        self.name = name
        self.datetime = datetime_obj

class Calendar:
    """
    Represents a calendar that can store and manage events.
    """
    def __init__(self):
        """
        Initializes a Calendar object with an empty list of events.
        """
        self.events = []

    def add_event(self, event):
        """
        Adds an event to the calendar.
        
        Args:
            event (CalendarEvent): The event to be added to the calendar.
        """
        self.events.append(event)

    def remove_event(self, event):
        """
        Removes an event from the calendar.
        
        Args:
            event (CalendarEvent): The event to be removed from the calendar.
        """
        self.events.remove(event)

    def get_events(self, date=None):
        """
        Returns a list of events on the specified date or all events if no date is provided.
        
        Args:
            date (date, optional): The date for which to retrieve events. Defaults to None.
        
        Returns:
            list: A list of events on the specified date or all events if no date is provided.
        """
        if date:
            return [event for event in self.events if event.datetime.date() == date]
        else:
            return self.events

    def print_calendar(self):
        """
        Prints all events in the calendar in the format "YYYY-MM-DD HH:MM - Event Name".
        """
        for event in self.events:
            print(f"{event.datetime.strftime('%Y-%m-%d %H:%M')} - {event.name}")

# Create a new calendar instance
calendar = Calendar()

try:
    # Attempt to load the device_id from the command-line argument as JSON
    device_id = json.loads(sys.argv[1])
except (IndexError, json.JSONDecodeError) as e:
    # If there is an error decoding the JSON or the argument is missing
    print(f"Error decoding JSON: {e}")
    # Handle the error, e.g., exit the script or provide a default value
    device_id = {'device_index': 0}

# Create a speech recognition instance
r = sr.Recognizer()

# Select the microphone using the device_index from the device_id dictionary
with sr.Microphone(device_index=device_id['device_index']) as source:
    print("Listening...")
    # Set the pause threshold for the recognizer
    r.pause_threshold = 1
    # Listen to the audio from the microphone and store it in the audio variable
    audio = r.listen(source)

# Initialize the ElevenLabs text-to-speech engine with the API key
client = ElevenLabs(
  api_key="44bd2fafea55e550c58548571fe9f64d"
)

# Set the wake-up keyword to "Alpha"
wake_word = "Alpha"

# Define a function to convert text to speech using the ElevenLabs API
def speak(text):
    # Generate audio from the given text using the "James Fitzgerald" voice and "eleven_multilingual_v2" model
    audio = client.generate(text=text, voice="James Fitzgerald", model="eleven_multilingual_v2")
    # Play the generated audio
    play(audio)

# Define a function to open a website in the default web browser
def open_website(url):
    # Open the specified URL in the default web browser
    webbrowser.open(url)
    # Speak a message indicating that the website is being opened
    speak("Opening website.")

# Define a function to tell the current time
def tell_time():
    # Get the current time as a string in the format "HH:MM AM/PM"
    time = datetime.datetime.now().strftime("%I:%M %p")
    # Speak the current time
    speak(f"The time is {time}.")

# Define a function to add an event to the calendar
def add_calendar_event(r):
    # Use the microphone to get input from the user
    with sr.Microphone(device_index=device_id['device_index']) as source:
        # Ask the user for the event name and recognize the speech
        speak("What is the name of the event?")
        event_name = r.recognize_google(r.listen(source))
        print(f"You said: {event_name}")

        # Ask the user for the event date and recognize the speech
        speak("What is the date of the event?") # Format Month, Day, Year is applicable
        event_date_str = r.recognize_google(r.listen(source))
        print(f"You said: {event_date_str}")

        # Split the date string into month, day, and year
        event_date_parts = event_date_str.split(" ")

        # Check if the date string has at least month and day
        if len(event_date_parts) < 2 or len(event_date_parts) > 3:
            speak("I'm sorry, I didn't understand the date format. Please try again.")
            return

        # Extract the month, day, and year from the date string
        event_month_str = event_date_parts[0].strip()
        event_day_str = event_date_parts[1].strip()
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

        # Ask the user for the event time and recognize the speech
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
    # Use the microphone to get input from the user
    with sr.Microphone(device_index=device_id['device_index']) as source:
        # Ask the user for the reminder text and recognize the speech
        speak("What is the reminder text?")
        reminder_text = r.recognize_google(r.listen(source))
        print(f"You said: {reminder_text}")

        # Ask the user for the reminder time and recognize the speech
        speak("What time would you like to set the reminder?") # Format Hour:Minute
        reminder_time = r.recognize_google(r.listen(source))
        print(f"You said: {reminder_time}")

        # Convert the reminder time to a datetime object
        reminder_datetime = datetime.datetime.strptime(reminder_time, "%H:%M")

        # Set the reminder
        # calendar.setreminder(reminder_text, reminder_datetime) # This is a placeholder function
        speak(f"I've set a reminder for '{reminder_text}' at {reminder_time}.")

def get_weather(city):
    # Set the API key and base URL for the OpenWeatherMap API
    api_key = "39c53008af40643aa03b01b0e27de931"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city + "&units=imperial"
    
    # Send a GET request to the API with the complete URL
    response = requests.get(complete_url)
    data = response.json()

    # Check if the API response has an error code
    if data["cod"] != "404":
        # Extract the weather description and temperature from the API response
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        
        # Return the weather information as a string
        return f"The weather in {city} is {weather} with a temperature of {temperature}°F."
    else:
        # Return an error message if the city is not found
        return f"Sorry, I couldn't find the weather information for {city}."

def gpt_math(
    inputtext="what is ten times 9 plus fifty five to the power of 7 and then all of that square rooted",
):
    # Create a Client object for the OpenAI API
    _client = Client()
    
    # Send a chat completion request to the OpenAI API with the given input text
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

    # Extract the Python code from the API response
    response = response.choices[0].message.content.replace("```python", "```")
    matches = re.findall(r"(?<=```).*?(?=```)", response, re.DOTALL)
    response = matches[0]

    print(response)
    
    try:
        # Temporarily set output into a string variable
        output = io.StringIO()
        sys.stdout = output
        
        # Execute the Python code
        exec(response)
        
        # Revert the output to the original stdout
        output_str = output.getvalue()
        sys.stdout = sys.__stdout__
        
        # Print and speak the output
        print(output_str)
        speak(output_str)
    except:
        # Handle any exceptions that occur during the code execution
        speak("I'm sorry, I couldn't calculate that expression.")

def ask_gpt(
    inputtext
):
    # Create a Client object for the OpenAI API
    _client = Client()
    
    # Send a chat completion request to the OpenAI API with the given input text
    response = _client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"""Respond to the following user prompt in a sentence or two:
    
{inputtext}            
""",
            }
        ],
    )

    # Extract the response from the API response
    response = response.choices[0].message.content
    
    try:
        # Print and speak the response
        print(response)
        speak(response)
    except:
        # Handle any exceptions that occur during the response processing
        speak("I'm sorry, can you say that again?")
        
def ask_wolframalpha(question, app_id = "TYJYRK-UVWT679K48"):
    """
    Queries WolframAlpha with the given question and returns the response text.

    Parameters:
    - question (str): The question to ask WolframAlpha.
    - app_id (str): The app ID obtained from WolframAlpha.
    """
    
    # Create a Client object for the OpenAI API
    _client = Client()
    
    # Send a chat completion request to the OpenAI API with the given question
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

    # Extract the WolframAlpha input string from the API response
    response = response.choices[0].message.content
    # Regex pattern to match everything between "&&"
    pattern = r'\&\&(.*?)\&\&'
    # Find all matches
    matches = re.findall(pattern, response)

    try:
        # Get the first match (the WolframAlpha input string)
        response = matches[0]
        
        # Instance of WolframAlpha client class with the app ID
        client = wolframalpha.Client(app_id)

        # Query WolframAlpha with the input string
        res = client.query(question)

        # Extract the text from the first result
        answer = next(res.results).text

        # Speak the answer
        speak(answer)
    except:
        # Handle any exceptions that occur during the WolframAlpha query
        speak("I'm sorry, I didn't understand that.")

def remove_calendar_event(r):
    # Use the microphone to get input from the user
    with sr.Microphone(device_index=device_id['device_index']) as source:
        # Ask the user for the name of the event to remove and recognize the speech
        speak("What is the name of the event you want to remove?")
        event_name = r.recognize_google(r.listen(source))
        print(f"You said: {event_name}")

        # Find the event in the calendar
        event_to_remove = next((event for event in calendar.events if event.name == event_name), None)
        if event_to_remove:
            # Remove the event from the calendar
            calendar.remove_event(event_to_remove)
            speak(f"Removed the event '{event_name}' from your calendar.")
        else:
            # Speak a message if the event is not found
            speak(f"I couldn't find an event named '{event_name}' in your calendar.")

def get_calendar_events(r):
    # Use the microphone to get input from the user
    with sr.Microphone(device_index=device_id['device_index']) as source:
        # Ask the user for the date of the events to retrieve and recognize the speech
        speak("What date would you like to see the events for?")
        event_date_str = r.recognize_google(r.listen(source))
        print(f"You said: {event_date_str}")

        # Parse the date string
        event_date_parts = event_date_str.split(" ")
        if len(event_date_parts) < 2 or len(event_date_parts) > 3:
            # Speak an error message if the date format is not understood
            speak("I'm sorry, I didn't understand the date format. Please try again.")
            return

        event_month_str = event_date_parts[0].strip()
        event_day_str = event_date_parts[1].strip()

        if len(event_date_parts) > 2:
            event_year = int(event_date_parts[2].strip())
        else:
            event_year = datetime.date.today().year

        event_day_str = event_day_str.rstrip("stndrdth")
        event_day = int(event_day_str)

        # Convert the month name to the corresponding number
        month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        event_month = next((i for i, month in enumerate(month_names) if month.lower() == event_month_str.lower()), None)
        if event_month is None:
            # Speak an error message if the month name is not recognized
            speak("I'm sorry, I didn't recognize that month name.")
            return

        # Create the event date object
        event_date = datetime.date(event_year, event_month + 1, event_day)
        
        # Get the events on the specified date
        events_on_date = calendar.get_events(event_date)

        if events_on_date:
            # Speak the events on the specified date
            speak(f"Here are the events on {event_date_str}:")
            for event in events_on_date:
                speak(f"{event.name} at {event.datetime.strftime('%I:%M %p')}")
        else:
            # Speak a message if there are no events on the specified date
            speak(f"There are no events scheduled for {event_date_str}.")

def gpt_goto_website(inputtext):
    # Create a Client object for the OpenAI API
    _client = Client()
    
    # Send a chat completion request to the OpenAI API with the given input text
    response = _client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"""I will ask you for a website url and you will give me the url surrounded by && like &&this&&. Do not give anything else but the website.

    {inputtext}
    """,
            }
        ],
    )

    # Extract the website URL from the API response
    response = response.choices[0].message.content
    # Regex pattern to match everything between "&&"
    pattern = r"\&\&(.*?)\&\&"
    # Find all matches
    matches = re.findall(pattern, response)

    print(response)
    
    try:
        # Get the first match (the website URL)
        response = matches[0]

        print(response)
        # Open the website URL
        open_website(response)

        # go to website here
    except:
        # Handle any exceptions that occur during the website opening
        print("uh oh")

# Define function to check the command and execute the appropriate action
def check_command(command, r):
    # Check if the command contains "open"
    if "open" in command.lower():
        # If "open" is found, pass the command to the gpt_goto_website function
        gpt_goto_website(command)
    # Check if the command contains "time"
    elif "time" in command.lower():
        # If "time" is found, call the tell_time function
        tell_time()
    # Check if the command contains "weather"
    elif "weather" in command.lower():
        # If "weather" is found, extract the city name from the command
        city = command.lower().split()[-1]
        # Get the weather information for the city
        weather_info = get_weather(city)
        # Speak the weather information
        speak(weather_info)
    # Check if the command contains "add" and "event"
    elif "add" in command.lower() and "event" in command.lower():
        # If "add" and "event" are found, call the add_calendar_event function
        add_calendar_event(r)
    # Check if the command contains "remove" and "event"
    elif "remove" in command.lower() and "event" in command.lower():
        # If "remove" and "event" are found, call the remove_calendar_event function
        remove_calendar_event(r)
    # Check if the command contains "get" and "event"
    elif "get" in command.lower() and "event" in command.lower():
        # If "get" and "event" are found, call the get_calendar_events function
        get_calendar_events(r)
    # Check if the command contains "set" and "reminder"
    elif "set" in command.lower() and "reminder" in command.lower():
        # If "set" and "reminder" are found, call the set_reminder function
        set_reminder(r)
    # Check if the command contains "google"
    elif "google" in command.lower():
        # If "google" is found, extract the search query from the command
        query = command.lower().replace("google", "").strip()
        if query:
            # Replace spaces with "+" in the query
            query = query.replace(" ", "+")
            # Construct the Google search URL
            url = f"https://www.google.com/search?q={query}"
            # Open the Google search URL
            open_website(url)
        else:
            # If no query is provided, ask for the search query
            speak("What would you like me to search for on Google?")
    # Check if the command contains "calculate"
    elif "calculate" in command.lower():
        # If "calculate" is found, pass the command to the gpt_math function
        gpt_math(command.lower().replace("calculate", "").strip())
    # Check if the command contains "wolfram"
    elif "wolfram" in command.lower():
        # If "wolfram" is found, pass the command to the ask_wolframalpha function
        ask_wolframalpha(command.lower().strip())
    else:
        # If no specific command is matched, treat it as a chat query
        query = command.lower()
        if query:
            print("THE HALLUCOGENS ARE KICKING IN")
            # Pass the chat query to the ask_gpt function
            ask_gpt(query)
        else:
            # If no query is provided, ask for the chat topic
            speak("What would you like to chat about?")
            
try:
    # Create a speech recognition instance and set the audio source
    r = sr.Recognizer()
    speak("Yes Sir?")
    with sr.Microphone(device_index=device_id['device_index']) as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    # Convert speech to text
    command = r.recognize_google(audio)
    print("You said: " + command)
        
    # Check the command and execute the appropriate action
    check_command(command, r)
        
    # Check if the command contains "goodbye" or "exit"
    if "goodbye" in command.lower() or "exit" in command.lower():
        # If "goodbye" or "exit" is found, speak a farewell message
        speak("Goodbye!")
    
except sr.UnknownValueError:
    # Handle the case when the speech recognition fails to understand the input
    speak("I'm sorry, I didn't understand that.")
except sr.RequestError as e:
    # Handle the case when the speech recognition fails to reach the Google servers
    speak("Sorry, I couldn't reach the Google servers. Check your internet connection.")