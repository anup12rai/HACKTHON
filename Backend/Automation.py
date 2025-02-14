from AppOpener import close,open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import os
import asyncio

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize Groq client
from groq import Groq
client = Groq(api_key=GroqAPIKey)

# System messages for AI
SystemChatBot = [{"role": "system", "content": "Hello, I am your AI assistant. Write content like professional letters, guides, or applications."}]
messages = []

# General response templates
professional_response = [
    "Your satisfaction is my top priority; feel free to reach out if there is anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
]

# Classes for parsing content (used later in scraping)
classes = [
    "zCubwf", "hgKELc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee",
    "tw-Data-text tw-text tw-text-small tw-ta", "IZ6rdc", "O5uR6d LTKOO", "vlzY6d",
    "webanswers-webanswers_table_webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt",
    "sXLaOE", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
]
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36'

# Function to perform Google search
def GoogleSearch(Topic):
    search(Topic)
    return True

# Function to generate and open content
def Content(Topic):

    
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])
  
    def ContentWritterAI(prompt):
        
        messages.append({"role": "user", "content": f"{prompt}' in a professional format."})
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    # Process and sanitize the topic
    Topic:str = Topic.replace("Content ", "")
    ContentByAI = ContentWritterAI(Topic)
    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()

              
    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")
    return True

# Function to perform YouTube search
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

# Function to play YouTube videos
def PlayYoutube(query):
    playonyt(query)
    return True
# Function to open applications
def OpenApp(app, sess=requests.session()):
    
    try:
        appopen(app,match_closest=True,output=True,throw_error = True)
        return True
    except:
        def extract_link(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser') 
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]

        def search_google(query):
            url = f'https://www.google.com/search?q={query}'
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve search result.")
            return None

        html = search_google(app)
        if html:
            link = extract_link(html)[0]
            webopen(link)
        return True
OpenApp("facebook")
# Function to close applications
def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True,output=True,throw_error=True)
            return True
        except:
            return False        
# System control for volume
def System(command):
    
    if command == "mute":
        keyboard.press_and_release('volume mute')
    elif command == "unmute":
        keyboard.press_and_release('volume mute')
    elif command == "volume up":
        keyboard.press_and_release('volume up')
    elif command == "volume down":
        keyboard.press_and_release('volume down')
    return True

# Asynchronous command translator
async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open"):
            if "open it" in command:
                pass
            if "open file" in command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open"))
                funcs.append(fun)
        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass    
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close"))
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play"))
            funcs.append(fun)
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content"))
            funcs.append(fun)
        elif command.splitlines("google search "):
            
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search"))
            funcs.append(fun)
        elif command.startswith("youtube search"):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search"))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system"))
            funcs.append(fun)  
        else:
            print(f"no function found.for{command}")
    results = await asyncio.gather(*funcs)
    for result in results:
        if isinstance(result,str):
            yield result
        else:
            yield result
                           
# Main automation function
# async def Automation(commands: list[str]):
    
#     async for result in TranslateAndExecute(commands):
#         pass
#     return True
if __name__ == "__main__":
    asyncio.run("youtube")