from flask import Flask, render_template, request, jsonify
import serial
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
from TextToSpeech import TextToSpeech
from timeee import function
import subprocess
from systeminstruction import System
from play_songs import play_youtube, skip_ads

app = Flask(__name__)

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")
list_of_songs = ["waven flag"]

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)
arduino = serial.Serial('COM5', 9600, timeout=1)

# Messages list and System ChatBot setup
messages = []
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

def load_chat_log():
    try:
        with open(r"Data/ChatLog.json", "r") as f:
            return load(f)
    except FileNotFoundError:
        with open(r"Data/ChatLog.json", "w") as f:
            dump([], f)
        return []

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def save_chat_log(messages):
    with open(r"Data/ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

def OpenNotepad(File):
    subprocess.Popen(["notepad.exe", File])

def Content(Topic):
    """Generates professional content and opens it in Notepad"""
    try:
        messages.append({"role": "user", "content": f"{Topic} in a professional format."})
        TextToSpeech("Sir, wait a sec, generating the content.")
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

        Answer = Answer.replace("</s>", "").strip()
        messages.append({"role": "assistant", "content": Answer})

        # Save content to a file
        filename = "Generated_Content.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(Answer)
        TextToSpeech("Have a look sir. The content is ready.")
        # Open file in Notepad
        OpenNotepad(filename)

        return Answer

    except Exception as e:
        return f"An error occurred: {e}"

def ControlLight(command):
    """Send a command to Arduino to control lights"""
    arduino.write(command.encode())  # Send command to Arduino
    response = arduino.readline().decode('utf-8').strip()  # Read response from Arduino
    return response

def ChatBot(Query):
    """This function sends the user query and handles light commands"""
    try:
        # Load chat log
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)

        messages.append({"role": "user", "content": f"{Query}"})

        # Check for light control commands
        if 'turn on light1' in Query.lower():
            response = ControlLight("light1_on")
        elif 'turn off light1' in Query.lower():
            response = ControlLight("light1_off")
        elif 'turn on light2' in Query.lower():
            response = ControlLight("light2_on")
        elif 'turn off light2' in Query.lower():
            response = ControlLight("light2_off")
        elif 'play' in Query.lower() or 'music' in Query.lower():
            response = play_youtube("waven flag")
        elif "open notepad" in Query.lower():
            OpenNotepad("Generated_Content.txt")
        else:
            response = AnswerModifier("Assistant is working.")

        return response

    except Exception as e:
        return f"An error occurred: {e}"

def save_messages():
    with open(r"Data\ChatLog.json", "w") as file:
        dump(messages, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = ChatBot(user_input)
    return jsonify({'response': response})

@app.route('/update_time', methods=['GET'])
def update_time():
    return jsonify({'time': RealtimeInformation()})

if __name__ == "__main__":
    app.run(debug=True)
