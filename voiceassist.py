import speech_recognition as sr
import pyttsx3
import smtplib
import requests
import datetime
import dateparser
import threading
import time

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
        return None

def send_email(to_address, subject, body):
    from_address = "kundusrijan003@gmail.com"
    password = "Srijan@14"

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(from_address, to_address, message)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        speak(f"Failed to send email: {str(e)}")

def get_weather(city):
    api_key = "54ae6d03f28d3774b1f59bf399b6da6e"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()

    if weather_data.get("cod") != 200:
        speak("City not found.")
        return

    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]
    speak(f"The weather in {city} is {weather_description} with a temperature of {temperature} degrees Celsius.")

def set_reminder(reminder, reminder_time):
    def reminder_thread(reminder, reminder_time):
        while True:
            now = datetime.datetime.now()
            if now >= reminder_time:
                speak(f"Reminder: {reminder}")
                break
            time.sleep(1)
    
    thread = threading.Thread(target=reminder_thread, args=(reminder, reminder_time))
    thread.start()

def main():
    speak("Hello! How can I assist you today?")
    
    while True:
        command = listen()
        if command:
            if "email" in command:
                speak("Who do you want to send the email to?")
                to_address = listen()
                speak("What is the subject?")
                subject = listen()
                speak("What should I say in the email?")
                body = listen()
                send_email(to_address, subject, body)
            
            elif "weather" in command:
                speak("Which city's weather would you like to know about?")
                city = listen()
                get_weather(city)
            
            elif "reminder" in command:
                speak("What is the reminder?")
                reminder = listen()
                speak("When should I remind you?")
                reminder_time_str = listen()
                reminder_time = dateparser.parse(reminder_time_str)
                if reminder_time:
                    set_reminder(reminder, reminder_time)
                    speak(f"Reminder set for {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    speak("I couldn't understand the date and time for the reminder.")
            
            elif "exit" in command or "stop" in command:
                speak("Goodbye!")
                break
            
            else:
                speak("I can help with sending emails, fetching weather, and setting reminders.")
        
        time.sleep(1)

if __name__ == "__main__":
    main()
