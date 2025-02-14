from groq import Groq
from json import load, dump
import datetime
import time
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from SpeechToText import SpeechRecognization
from TextToSpeech import TextToSpeech
import os

# Suppress TensorFlow Lite XNNPACK delegate warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Predefined song list
list_of_songs = ["give me sunshine", "peelo lofi", "7 years", "love me like you do"]

# Selenium WebDriver setup
options = webdriver.ChromeOptions()
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Load chat log
try:
    with open("Data/ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open("Data/ChatLog.json", "w") as f:
        dump([], f)

# Real-time information function
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    return f"Current day: {current_date_time.strftime('%A')}, Time: {current_date_time.strftime('%H:%M')}"

# Answer modifier function
def AnswerModifier(Answer):
    return '\n'.join([line for line in Answer.split('\n') if line.strip()])

# YouTube music playing function
def play_youtube(query):
    if not query:
        TextToSpeech("Error: No query provided for playing.")
        return False
    
    driver.get(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
    time.sleep(3)
    try:
        video = driver.find_element(By.CSS_SELECTOR, "a#video-title")
        video.click()
        TextToSpeech(f"Playing {query}")
        print(f"Playing: {query}")
        time.sleep(5)
        skip_ads()
    except Exception as e:
        print("Error playing video:", e)
        TextToSpeech("Could not play the video.")

def skip_ads():
    try:
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button").click()
        print("Ad skipped!")
    except:
        print("No ads detected.")

# Chatbot function
def ChatBot(Query):
    try:
        with open("Data/ChatLog.json", "r") as f:
            messages = load(f)
        messages.append({"role": "user", "content": Query})

        # Check if the query is related to music
        if any(keyword in Query.lower() for keyword in ["play music", "play song", "i am tired"]):
            TextToSpeech("Sir, which song should I play, or can I play from the listed songs?")
            user_input = input("Enter the commsnd: ")
            if "list" in user_input.lower() or "favorite" in user_input.lower():
                play_youtube(list_of_songs[0])
            else:
                play_youtube(user_input)
            return "Playing song..."

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "system", "content": f"Hello, I am {Username}, You are {Assistantname}."},
                      {"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True
        )

        Answer = "".join([chunk.choices[0].delta.content for chunk in completion if chunk.choices[0].delta.content])
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        with open("Data/ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return "Bot: " + AnswerModifier(Answer)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        with open("Data/ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query)

# Main execution
if __name__ == "__main__":
    while True:
        user_input = input("Enter your Question: ")
        print(ChatBot(user_input))
