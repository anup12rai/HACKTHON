import asyncio
import websockets
import json
import serial
import subprocess
import datetime
from groq import Groq
from dotenv import dotenv_values
from TextToSpeech import TextToSpeech
from systeminstruction import System
from play_songs import play_youtube
from json import load, dump

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")
list_of_songs = ["waven flag"]

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Serial connection for Arduino
arduino = serial.Serial('COM5', 9600, timeout=1)

# Initialize user sessions
user_sessions = {}

# Messages list and System ChatBot setup
System = System
SystemChatBot = [{"role": "system", "content": System}]

def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data = f"Please use this real-time information if needed,\n"
    data += f"Current day: {day}\nDate: {date} {month} {year}, Time: {hour}:{minute}\n"
    data += f"Time: {hour} hour: {minute} minutes: {second} seconds.\n"
    return data

def ControlLight(command):
    """Send a command to Arduino to control lights"""
    arduino.write(command.encode())  # Send command to Arduino
    response = arduino.readline().decode('utf-8').strip()  # Read response from Arduino
    return response

def Content(Topic):
    """Generates professional content and opens it in Notepad"""
    try:
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + [{"role": "user", "content": f"{Topic} in a professional format."}],
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
        Answer = Answer.replace("</s>", "").strip()

        filename = "Generated_Content.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(Answer)
        
        TextToSpeech("Have a look sir. The content is ready.")
        subprocess.Popen(["notepad.exe", filename])

        return Answer
    except Exception as e:
        return f"An error occurred: {e}"

async def handle_connection(websocket, path):
    user_id = str(id(websocket))  # Unique identifier for each user session
    print(f"New connection: {user_id}")

    # Initialize a unique chat session for the user
    user_sessions[user_id] = {
        'messages': SystemChatBot,
    }

    try:
        async for message in websocket:
            data = json.loads(message)
            user_input = data.get("input", "")
            print(f"Received input from {user_id}: {user_input}")

            # Handle light control commands
            if 'turn on light1' in user_input.lower():
                response = ControlLight("light1_on")
            elif 'turn off light1' in user_input.lower():
                response = ControlLight("light1_off")
            elif 'turn on light2' in user_input.lower():
                response = ControlLight("light2_on")
            elif 'turn off light2' in user_input.lower():
                response = ControlLight("light2_off")
            # Handle YouTube related commands
            elif any(keyword in user_input.lower() for keyword in ["play music", "play song", "i am tired"]):
                TextToSpeech("Sir, which song should I play, or can I play from the listed songs?")
                play_youtube(list_of_songs[0])  # Play a default song or user input
                response = "Playing song..."

            # Handle content generation
            elif "application" in user_input.lower() or "create" in user_input.lower():
                content = Content(user_input)  # Generate content and open in Notepad
                response = content

            else:
                # Send request to Groq API for other queries
                completion = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=user_sessions[user_id]['messages'] + [{"role": "system", "content": RealtimeInformation()}],
                    max_tokens=1024,
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
                user_sessions[user_id]['messages'].append({"role": "assistant", "content": Answer})

                response = Answer

            # Send response back to the user
            await websocket.send(json.dumps({"response": response}))

    except websockets.exceptions.ConnectionClosed:
        print(f"Connection closed: {user_id}")

    finally:
        # Clean up the session
        if user_id in user_sessions:
            del user_sessions[user_id]
async def handle_connection(connection, path):
    print(f"New connection: {path}")
    try:
        async for message in connection:
            print(f"Received message: {message}")
            await connection.send(f"Hello! You said: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")

# --- WebSocket Server ---
async def main():
    server = await websockets.serve(handle_connection, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

# Start WebSocket server
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Server shutting down...")
finally:
    if arduino and arduino.is_open:
        arduino.close()
        print("Serial connection closed.")
