from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
from TextToSpeech import TextToSpeech
from Model import FirstLayerDDM
from play_songs import play_youtube,skip_ads
import os
import subprocess
from timeee import function
import re
from asyncio import run
from systeminstruction import System

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")
list_of_songs = ["give me sunshine"]
# Initialize Groq client
client = Groq(api_key=GroqAPIKey)
Function = ["open", "close", "play", "system", "google search", "youtube search"]

# System message configuration
System = System
messages = []
SystemChatBot = [
    {"role": "system", "content": System}
]

# Load chat log
def load_chat_log():
    try:
        with open(r"Data/ChatLog.json", "r") as f:
            return load(f)
    except FileNotFoundError:
        with open(r"Data/ChatLog.json", "w") as f:
            dump([], f)
        return []
# Save chat log
def save_chat_log(messages):
    with open(r"Data/ChatLog.json", "w") as f:
        dump(messages, f, indent=4)
def OpenNotepad(File):
    subprocess.Popen(["notepad.exe", File])

# Function to generate content (e.g., application letter) in a professional format
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
# Real-time information function
def RealtimeInformation():
    """This function returns the real-time date and time information."""
    try:
        current_date_time = datetime.datetime.now()
        return (
            f"Please use this real-time information if needed,\n"
            f"Current day: {current_date_time.strftime('%A')}\n"
            f"Date: {current_date_time.strftime('%d %B %Y')}, Time: {current_date_time.strftime('%H:%M:%S')}\n"
        )
    except Exception as e:
        return f"An error occurred while fetching real-time information: {e}"


def AnswerModifier(answer):
    # Remove asterisks (*) from the answer
    clear_answer = re.sub(r'[*]', '', answer)
    
    # Split the answer into lines, remove empty lines, and join the result
    lines = clear_answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)
def ChatBot(Query):
    """This function sends the user query."""
    try:
        # Load chat log
        with open("Data/ChatLog.json", "r") as f:
            messages = load(f)

        # Check for YouTube related queries or "I am tired"
        if any(keyword in Query.lower() for keyword in ["play music", "play song", "i am tired"]):
            TextToSpeech("Sir, which song should I play, or can I play from the listed songs?")
            user_input = input("Enter the query: ")
            
            # If user asks for a list or their favorite song
            if "list" in user_input.lower() or "favorite" in user_input.lower():
                # Assuming 'list_of_songs' is predefined with a list of songs
                play_youtube(list_of_songs[0])  # Play the first song in the list
            else:
                play_youtube(user_input)  # Play the song user requests
            return "Playing song..."

        # If the query involves content generation, call Content function
        if "application" in Query.lower() or "create" in Query.lower() or "write" in Query.lower() or "code" in Query.lower() or "program" in Query.lower() or "letter" in Query.lower():
            Content(Query)  # This will handle everything related to Notepad generation
            return ""  # Return an empty string because content is handled in Notepad

        # Otherwise, continue the normal chatbot interaction
        messages.append({"role": "user", "content": Query})

        # Send request to Groq API
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        # Process completion response
        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        # Clean up answer
        Answer = Answer.replace("</s>", "").strip()
        messages.append({"role": "assistant", "content": Answer})

        # Save updated chat log
        with open("Data/ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        # Convert answer to speech
        TextToSpeech(Answer)

        return "Bot: " + Answer

    except Exception as e:
        return f"An error occurred: {e}"

def MainExecution():
    print("Listening...")
    Query = input("Enter the command:")#............................................................
    Decision = FirstLayerDDM(Query)
    print(f"Decision: {Decision}\n")

    TaskExecution = False
    G = any(decision.startswith("general") for decision in Decision)
    R = any(decision.startswith("realtime") for decision in Decision)
    Merge_query = [
        "".join(decision.split()[1:]) for decision in Decision if decision.startswith("general") or decision.startswith("realtime")
    ]

    # if not TaskExecution:
    #     for decision in Decision:
    #         if any(decision.startswith(func) for func in Function):
    #             run(Automation(list(Decision)))
    #             TaskExecution = True

    if G and R:
        print("Searching...")
        print(f"{Assistantname}: {Answer}")
        # Get real-time information and pass it to TextToSpeech
        Answer = RealtimeInformation()
        TextToSpeech(Answer)

    else:
        for decision in Decision:
            if decision.startswith("general"):
                print("Thinking...")
                print(f"{Assistantname}: {Answer}")
                Answer = ChatBot(decision.replace("general", ""))
                

            # elif decision.startswith("realtime"):
            #     print("Searching...")
            #     print(f"{Assistantname}: {Answer}")
            #     Answer = RealtimeSearchEngine(decision.replace("realtime", ""))
                

            elif decision == "exit":
                Answer = ChatBot("ok bye sir")
                print(Answer)
                TextToSpeech(Answer)
                break

# Main function
if __name__ == "__main__":
    TextToSpeech(function())
    while True:
        user_input = input("Enter the command: ")
        print(ChatBot(user_input))
