import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#todo: weather api- jslibrary
#todo:news api

def ai(prompt):
    openai.api_key = apikey
    text1=f"Openai response for prompt:  {prompt}\n**********\n\n"

    response = openai.ChatCompletion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    #todo:wrP THIS INSIDE A TRY CATCH BLOCK
    #print(response["choice"][0]["text"])
    text1+=response["choice"][0]["text"]
    if not os.path.exists("openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt","w") as f:
        f.write(text1)

def chat(text):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"sri: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

services = {
    "instagram": {
        "url": "https://www.instagram.com/",
        "username_field_name": "username",
        "password_field_name": "password",
        "login_button_name": "Log In",
    },
    "gmail": {
        "url": "https://www.gmail.com/",
        "username_field_name": "identifier",
        "password_field_name": "password",
        "login_button_name": "Next",
    },
}
def login_to_service(service_name, email, password):
    if service_name.lower() not in services:
        print("Service not supported.")
        return

    service = services[service_name.lower()]
    driver_path = r"C:\Users\Murthy ESSR\Downloads\chromedriver_win32\chromedriver.exe"

    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.get(service[url])

    driver.implicitly_wait(10)
    email_field = driver.find_element_by_name(service["username_field_name"])
    email_field.send_keys(email)
    email_field.send_keys(Keys.ENTER)

    password_field = driver.find_element_by_name(service["password_field_name"])
    password_field.send_keys(password)
    password_field.send_keys(Keys.ENTER)
    driver.implicitly_wait(10)

    driver.quit()

def play_youtube_song(song_name):
    youtube_url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"
    webbrowser.get("chrome").open(youtube_url)
def say(text):
    engine = pyttsx3.init()
    #while 1:
    engine.say(text)
    engine.runAndWait()

def takecomd():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold =0.5
        audio= r.listen(source)
        try:
            print("And trying to understand what you say:")
            query= r.recognize_google(audio,language= "en-in")
            print(f"user said: {query}")
            return query
        except Exception as e:
            return "some error occured,please try again. my apologies"

if __name__ == '__main__':
    print('PyCharm')
    say("hello i am ES your assistant")
    webbrowser.register('chrome', None,
                        webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
    while True:
        print("listening:")
        text= takecomd()
        #print("Recognized Text:", text)
        sites=[["youtube","https://www.youtube.com"],
               ["wiki","https://www.wikipedia.com"],
               ["google","https://www.google.com"],
               ["music",r"C:\Users\Murthy ESSR\Downloads\Aradhya.mp3"],
               ["whatsapp","https://web.whatsapp.com"],
               ["instagram","https://www.instagram.com"],
               ["gmail","https://mail.google.com/mail"]]
        for site in sites:
            if f"Open {site[0]}".lower() in text.lower():
                say(f"opening {site[0]}..")
                if site[0] == "music":
                    musicpath = site[1]
                    os.startfile(musicpath)
                else:
                    webbrowser.get("chrome").open(site[1])

        if "login to " in text.lower():
            service_name = text.lower().replace("login to", "").strip()
            if service_name in services:
                say(f"Sure, please provide your {service_name} email and password.")
                say(f"What is your {service_name} email?")
                email = takecomd()

                say(f"What is your {service_name} password?")
                password = takecomd()

                say(f"Logging in to {service_name}...")
                login_to_service(service_name, email, password)
            else:
                say("Service not supported. Please try again.")

        elif "play" in text.lower() and "song" in text.lower():
            song_name = text.lower().replace("play", "").replace("song", "").strip()
            say(f"playing {song_name} on YouTube...")
            play_youtube_song(song_name)

        elif "the time" in text.lower():
            strfTime=datetime.datetime.now().strftime("%H:%M:%S")
            say(f"the time is {strfTime}")
        # we can create one similar to sites for apps either by lists or dictionary
        elif "open adobe".lower() in text.lower():
            os.system('start "" "C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe"')

        elif "using artificial intelligence".lower() in text.lower():
            ai(prompt=text)
        elif "reset chat".lower() in text.lower():
            chatStr = ""

        elif "stop chatting" in text.lower():
            exit()
        else:
            print("Chatting...")
            #chat(text)

        '''
        METHOD 1 OF OPENING MUSIC
        if "open music " in text.lower():
            musicpath=r"C:\\Users\Murthy ESSR\Downloads\Aradhya.mp3"
            os.startfile(musicpath)
            METHOD 2- FOR THIS USE IMPORT SUBPROCESS
            mediaplypath=r"path_to_ply.exc"
            try:
                os.startfile(musicpath)
                subprocess.run([mediaplypath, musicpath], check=True)
            except subprocess.CalledProcessError as e:
                print("Error occurred while playing the audio:", e)
                '''
                #os.system(f"\"{mediaplypath}\" \"{musicpath}\"")
        #say(text)





