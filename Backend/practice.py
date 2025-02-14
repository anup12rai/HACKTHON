import asyncio
import websockets
import json
import serial
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
from TextToSpeech import TextToSpeech
from systeminstruction import System
from play_songs import play_youtube

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Arduino connection
arduino = serial.Serial('COM5', 9600, timeout=1)

# System ChatBot setup
SystemChatBot = [{"role": "system", "content": System}]

def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d %B %Y")
    time = current_date_time.strftime("%H:%M:%S")
    return f"Today is {day}, {date}, Time: {time}."

def load_chat_log():
    try:
        with open("Data/ChatLog.json", "r") as f:
            return load(f)
    except FileNotFoundError:
        return []

def save_chat_log(messages):
    with open("Data/ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

def ControlLight(command):
    arduino.write(command.encode())
    return arduino.readline().decode('utf-8').strip()

def ChatBot(user_input):
    try:
        messages = load_chat_log()
        messages.append({"role": "user", "content": user_input})

        if 'turn on light' in user_input.lower():
            response = ControlLight("light_on")
        elif 'turn off light' in user_input.lower():
            response = ControlLight("light_off")
        elif 'play song' in user_input.lower():
            play_youtube("waving flag")
            response = "Playing song."
        else:
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
                max_tokens=1024,
                temperature=0.7,
                top_p=1,
                stream=False
            )
            response = completion.choices[0].message.content
            messages.append({"role": "assistant", "content": response})
            save_chat_log(messages)
            TextToSpeech(response)
        
        return response
    except Exception as e:
        return f"Error: {str(e)}"

async def handler(websocket, path):
    async for message in websocket:
        try:
            data = json.loads(message)
            user_input = data.get("message", "")

            if not user_input:
                response_data = {"error": "Invalid input"}
            else:
                response_text = ChatBot(user_input)
                response_data = {"response": response_text}

            await websocket.send(json.dumps(response_data))
        except Exception as e:
            await websocket.send(json.dumps({"error": str(e)}))

async def main():
    async with websockets.serve(handler, "localhost", 5000):
        await asyncio.Future()  # Keep the server running

asyncio.run(main())
