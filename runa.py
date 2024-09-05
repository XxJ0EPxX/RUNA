import spoty
import AVMSpeechMath as sm
import speech_recognition as sr
import pyttsx3
import pywhatkit
import json
import os
import pygetwindow as gw  # Importar pygetwindow
from datetime import datetime, date, timedelta
import wikipedia
import pyjokes
from time import time
import app_launcher
from datetime import datetime, timedelta
from threading import Timer
import pygame 

start_time = time()
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Nombre del asistente virtual
#RUNA = Responsive User Navigation Assistant
name = 'runa'
attemts = 0

# Llaves
with open('keys.json') as json_file:
    keys = json.load(json_file)

# Colores
green_color = "\033[1;32;40m"
red_color = "\033[1;31;40m"
normal_color = "\033[0;37;40m"

# Obtener voces y configurar la primera de ellas
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Editando la configuración predeterminada
engine.setProperty('rate', 178)
engine.setProperty('volume', 0.7)

day_es = [line.rstrip('\n') for line in open('day_es.txt')]
day_en = [line.rstrip('\n') for line in open('day_en.txt')]

def iterateDays(now):
    for i in range(len(day_en)):
        if day_en[i] in now:
            now = now.replace(day_en[i], day_es[i])
    return now

def getDay():
    now = date.today().strftime("%A, %d de %B del %Y").lower()
    return iterateDays(now)

def getDaysAgo(rec):
    value = ""
    if 'ayer' in rec:
        days = 1
        value = 'ayer'
    elif 'antier' in rec:
        days = 2
        value = 'antier'
    else:
        rec = rec.replace(",", "")
        rec = rec.split()
        days = 0

        for i in range(len(rec)):
            try:
                days = float(rec[i])
                break
            except:
                pass
    
    if days != 0:
        try:
            now = date.today() - timedelta(days=days)
            now = now.strftime("%A, %d de %B del %Y").lower()

            if value != "":
                return f"{value} fue {iterateDays(now)}"
            else:
                return f"Hace {days} días fue {iterateDays(now)}"
        except:
            return "Aún no existíamos"
    else:
        return "No entendí"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    status = False

    with sr.Microphone() as source:
        print(f"{green_color}({attemts}) Escuchando...{normal_color}")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        rec = ""

        try:
            rec = r.recognize_google(audio, language='es-ES').lower()
            
            if name in rec:
                rec = rec.replace(f"{name} ", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                status = True
            else:
                print(f"Vuelve a intentarlo, no reconozco: {rec}")
        except:
            pass
    return {'text': rec, 'status': status}

def take_note():
    speak("¿Qué quieres que anote?")
    note = get_audio()['text']
    
    if note:
        with open("notas.txt", "a") as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {note}\n")
        speak("Nota guardada.")

def send_whatsapp_message():
    speak("¿A quién deseas enviar el mensaje?")
    contact = get_audio()['text']
    
    speak("¿Cuál es el mensaje?")
    message = get_audio()['text']
    
    if contact and message:
        try:
            speak(f"Voy a enviar un mensaje a {contact}. Por favor, dime el número de teléfono.")
            number = get_audio()['text']
            
            # Filtrar el número para que solo contenga dígitos
            number = ''.join(filter(str.isdigit, number))
            
            if len(number) >= 9:  # Asegurarse de que el número tenga al menos 9 dígitos (Perú)
                full_number = f"+51{number}"
                speak(f"Enviando mensaje al número {full_number}")
                
                # Enviar el mensaje de inmediato
                pywhatkit.sendwhatmsg_instantly(full_number, message)
                speak("Mensaje enviado correctamente.")
            else:
                speak("El número de teléfono no es válido.")
        except Exception as e:
            print(f"Error al enviar el mensaje: {e}")
            speak("Ocurrió un error al enviar el mensaje.")
    else:
        speak("No entendí el contacto o el mensaje.")

def get_alarm_time():
    speak("¿A qué hora quieres establecer la alarma? Por favor, di la hora en formato de 12 horas, por ejemplo, 02:30 PM.")
    alarm_time = get_audio()['text']
    
    try:
        alarm_time_obj = datetime.strptime(alarm_time, '%I:%M %p')
        now = datetime.now()
        alarm_today = now.replace(hour=alarm_time_obj.hour, minute=alarm_time_obj.minute, second=0, microsecond=0)
        
        if alarm_today < now:
            alarm_today += timedelta(days=1)  # Si la hora ya pasó hoy, establecerla para el día siguiente
        
        return alarm_today
    except Exception as e:
        print(f"Error al obtener la hora de la alarma: {e}")
        speak("No entendí la hora de la alarma. Por favor, inténtalo de nuevo.")
        return None

def set_alarm(alarm_time):
    if alarm_time:
        time_diff = (alarm_time - datetime.now()).total_seconds()
        speak(f"Alarma configurada para las {alarm_time.strftime('%I:%M %p')}.")
        Timer(time_diff, alarm_ring).start()  # Esperar hasta que la alarma suene
    else:
        speak("No se pudo configurar la alarma.")

def alarm_ring():
    speak("¡Es hora de despertar!")
    print(f"{green_color} ¡ALARMA SONANDO! {normal_color}")

def stop_alarm():
    if pygame.mixer.music.get_busy():  # Verificar si la música está sonando
        pygame.mixer.music.stop()
        speak("Alarma desactivada.")
    else:
        speak("No hay ninguna alarma sonando.")

while True:
    rec_json = get_audio()

    rec = rec_json['text']
    status = rec_json['status']

    if status:
        if 'estas ahi' in rec:
            speak('Por supuesto')

        elif 'reproduce' in rec:
            if 'spotify' in rec:
                music = rec.replace('reproduce en spotify', '')
                speak(f'Reproduciendo {music}')
                spoty.play(keys["spoty_client_id"], keys["spoty_client_secret"], music)
            else:
                music = rec.replace('reproduce', '')
                speak(f'Reproduciendo {music}')
                pywhatkit.playonyt(music)

        elif 'que' in rec:
            if 'hora' in rec:
                hora = datetime.now().strftime('%I:%M %p')
                speak(f"Son las {hora}")

            elif 'dia' in rec:
                if 'fue' in rec:
                    speak(f"{getDaysAgo(rec)}")
                else:
                    speak(f"Hoy es {getDay()}")

        elif 'busca' in rec:
            order = rec.replace('busca', '')
            wikipedia.set_lang("es")
            info = wikipedia.summary(order, 1)
            speak(info)

        elif 'chiste' in rec:
            chiste = pyjokes.get_joke("es")
            speak(chiste)

        elif 'cuanto es' in rec:
            speak(sm.getResult(rec))

        elif 'nota' in rec:
            take_note()

        elif 'mensaje' in rec:
            send_whatsapp_message()

        elif 'alarma' in rec:
            alarm_time = get_alarm_time()
            set_alarm(alarm_time)

        elif 'desactiva alarma' in rec:
            stop_alarm()

        if 'abre' in rec:
            app_name = rec.replace('abre ', '')
            response = app_launcher.open_application(app_name)
            speak(response)

        elif 'cierra' in rec:
            app_name = rec.replace('cierra ', '')
            response = app_launcher.close_application(app_name)
            speak(response)

        elif 'descansa' in rec:                                                                                                         
            speak("Saliendo...")
            break

        else:
            print(f"Vuelve a intentarlo, no reconozco: {rec}")
        
        attemts = 0
    else:
        attemts += 1

print(f"{red_color} PROGRAMA FINALIZADO CON UNA DURACIÓN DE: { int(time() - start_time) } SEGUNDOS {normal_color}")