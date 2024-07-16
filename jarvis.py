import openai
import speech_recognition as sr 
import pyttsx3
import time
import os
import datetime
import requests

# Initialize OpenAI API
openai.api_key ="sk-proj-VHYLxUFW11LF55dtrDnlT3BlbkFJ0QoHKHYENeXh2M1UXmb9"

# Initialize the text to speech engine 
engine=pyttsx3.init()

def transcribe_audio_to_test(filename):
    recogizer=sr.Recognizer()
    with sr.AudioFile(filename)as source:
        audio=recogizer.record(source) 
    try:
        return recogizer.recognize_google(audio, language="es")
    except:
        print("No se que ha pasado")

def generate_response(prompt):
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=4000,
        temperature=0.5,
    )
    return response.choices[0].text

# Set Spanish voice for text-to-speech engine
voices = engine.getProperty('voices')
spanish_voice = None
for voice in voices:
    if "spanish" in voice.languages:
        spanish_voice = voice.id
if spanish_voice is not None:
    engine.setProperty('voice', spanish_voice)

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def print_user_input(text):
    print(f"Tu dijiste: {text}")

def open_application(text):
    if "abre" in text.lower():
        app_name = text.split(" ")[1]
        try:
            if app_name in ["google", "chrome", "navegador"]:
                os.startfile("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
            elif app_name in ["youtube", "yt"]:
                os.startfile("https://www.youtube.com")
            elif app_name in ["calculadora", "calc"]:
                os.startfile("calc.exe")
            elif app_name in ["bloque de notas", "notas"]:
                os.startfile("notepad.exe")
            elif app_name in ["word", "documento"]:
                os.startfile("winword.exe")
            elif app_name in ["excel", "hoja de cálculo"]:
                os.startfile("excel.exe")
            elif app_name in ["powerpoint", "presentación"]:
                os.startfile("start powerpnt.exe")
            elif app_name in ["microsoft edge", "edge"]:
                os.startfile("start edge.exe")
            elif app_name in ["microsoft teams", "teams"]:
                os.startfile("start teams.exe")
            elif app_name in ["microsoft office", "office"]:
                os.startfile("start office.exe")
            elif app_name in ["microsoft outlook", "correo"]:
                os.startfile("start outlook.exe")
            elif app_name in ["microsoft windows media player", "reproductor de música"]:
                os.startfile("start wmplayer.exe")
            elif app_name in ["microsoft paint", "pintura"]:
                os.startfile("start mspaint.exe")
            elif app_name in ["microsoft groove music", "música groove"]:
                os.startfile("start groovemusic.exe")
            elif app_name in ["microsoft photos", "fotos"]:
                os.startfile("start photos.exe")
            elif app_name in ["microsoft movies & tv", "películas y tv"]:
                os.startfile("start moviesandtv.exe")
            elif app_name in ["microsoft voice recorder", "grabadora de voz"]:
                os.startfile("start soundrecorder.exe")
            elif app_name in ["microsoft your phone", "tu teléfono"]:
                os.startfile("start yourphone.exe")
            elif app_name in ["microsoft 3d viewer", "visor 3d"]:
                os.startfile("start 3dviewer.exe")
            elif app_name in ["microsoft sticky notes", "notas adhesivas"]:
                os.startfile("start stickynotes.exe")
            else:
                speak_text("Lo siento, no puedo abrir esa aplicación")
        except:
            speak_text("Lo siento, no puedo abrir esa aplicación")
    else:
        speak_text("No entiendo, ¿qué aplicación deseas abrir?")

def get_weather(city):
    api_key = "fd3a8e97cd5ea84f8f2e6c4b09ef4eb9"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
       "units": "metric",
        "lang": "es"
    }
    response = requests.get(base_url, params=params)
    weather_data = response.json()
    return weather_data

def speak_weather(text):
    city = text.split(" ")[1]
    weather_data = get_weather(city)
    if weather_data:
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        speak_text(f"El clima en {city} es de {temperature} grados Celsius con {description}.")
    else:
        speak_text("No puedo obtener el clima para esa ciudad.")

def open_weather(text):
    if "clima" in text.lower():
        speak_weather(text)
    else:
        speak_text("No entiendo, ¿qué ciudad deseas saber el clima?")

def stop_program(text):
    if "detente" in text.lower():
        speak_text("Adiós")
        exit()

def greet_user():
    current_time = datetime.datetime.now().time()
    if current_time.hour < 12:
        speak_text("Buenos días")
    elif current_time.hour < 18:
        speak_text("Buenas tardes")
    else:
        speak_text("Buenas noches")
    speak_text("Soy Jarvis tu asistente de voz.¿En qué puedo ayudarte hoy?")

def main():
    greet_user()
    while True:
        #Record audio
        filename ="input.wav"
        with sr.Microphone() as source:
            recognizer=sr.Recognizer()
            source.pause_threshold=1
            audio=recognizer.listen(source,phrase_time_limit=None,timeout=None)
            with open(filename,"wb")as f:
                f.write(audio.get_wav_data())
        speak_text("Grabación completa")
        #Transcript audio to text 
        text=transcribe_audio_to_test(filename)
        if text:
            print_user_input(text)
            print(f"Tú: {text}")
            
            #Generate the response
            response = generate_response(text)
            print(f"Asistente: {response}")
                
            #Read response using GPT3
            speak_text(response)
            
            #Open application if requested
            open_application(text)
            
            #Get weather if requested
            open_weather(text)
            
            #Stop program if requested
            stop_program(text)

if __name__=="__main__":
    main()