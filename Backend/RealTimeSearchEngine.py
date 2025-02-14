from googleapiclient.discovery import build
import time
from dotenv import dotenv_values
import json
import datetime
from groq import Groq

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")
GoogleAPIKey = env_vars.get("GoogleAPIKey")
SearchEngineID = env_vars.get("SearchEngineID")

# Initialize Groq API client
client = Groq(api_key=GroqAPIKey)

# Define system message template
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Initialize chat log
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = json.load(f)
except:
    with open(r"Data\ChatLog.json", "w") as f:
        json.dump([], f)

# Function for Google Custom Search
def GoogleSearch(query):
    # Initialize the Google Custom Search API
    service = build("customsearch", "v1", developerKey=GoogleAPIKey)
    # Perform the search
    res = service.cse().list(q=query, cx=SearchEngineID).execute()

    Answer = f"The main points from the search results for '{query}' are:\n[start]\n"
    for item in res.get("items", []):
        # Include only title and snippet (description)
        Answer += f"Title: {item['title']}\nDescription: {item['snippet']}\n\n"
    Answer += "[end]\n"
    return Answer

# Function to clean and modify the answer
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]  # Corrected line name
    modified_answer = "\n".join(non_empty_lines)  # Fixed .json() to .join()
    return modified_answer

# Function to generate real-time information (date, time, etc.)
def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data += f"Use the real-time information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {day}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hour, {minute} minutes, {second} seconds.\n"
    return data  # Make sure this returns the data

# Main function for real-time search engine and chatbot interaction
def RealtimeSearchEngine(prompt):
    global messages
    with open(r"Data\ChatLog.json", "r") as f:
        messages = json.load(f)
    messages.append({"role": "user", "content": f"{prompt}"})
    # Store search results here
    search_results = GoogleSearch(prompt)
    messages.append({"role": "system", "content": search_results})  # Add search results to SystemChatBot
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages + [{"role": "system", "content": Information()}],
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )
    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})
    with open(r"Data\ChatLog.json", "w") as f:
        json.dump(messages, f, indent=4)
    return AnswerModifier(Answer=Answer)

# Main loop for user input
if __name__ == "__main__":
    while True:
        prompt = input("You: ")
        print(RealtimeSearchEngine(prompt))
        time.sleep(2)  # Adding a delay between requests to avoid rate-limiting
