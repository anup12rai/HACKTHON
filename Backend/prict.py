import os
import asyncio
import websockets
import json
import requests
from dotenv import dotenv_values
from groq import Groq

# Setup the chatbot
def setup_chatbot():
    try:
        env_vars = dotenv_values(".env")
        GroqAPIKey = env_vars.get("GroqAPIKey")

        if not GroqAPIKey:
            raise ValueError("GroqAPIKey not found in .env file")
        
        client = Groq(api_key=GroqAPIKey)
        return client
    except Exception as e:
        print(f"Error setting up chatbot: {e}")
        return None

# Function to handle chatbot response
def get_chatbot_response(client, query):
    try:
        system_instruction = "You are a helpful assistant."
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": query}
        ]
        
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=False,
        )
        
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Handle query function
async def handle_query(query, client):
    if query in ["1", "chatbot"]:
        response_content = "Chatbot started"
    elif query in ["2", "smart home"]:
        response_content = "Switching to Smart Home Assistant..."
        # mainxer()  # Uncomment if mainxer function is defined
    elif query in ["3", "weather"]:
        response_content = "Weather feature is under construction."
    else:
        response_content = get_chatbot_response(client, query)

    response = {"type": "response", "content": response_content}
    return json.dumps(response)

# Handle incoming WebSocket messages
async def handle_message(websocket, message, client):
    try:
        data = json.loads(message)
        query = data.get("content", "").strip()

        if not query:
            return None
        if query == "exit":
            return "exit"

        response = await handle_query(query, client)
        return response
    except Exception as e:
        return json.dumps({"type": "error", "content": str(e)})

# WebSocket connection handler
async def handle_connection(websocket, path):
    print("Client connected")
    initial_message = {"type": "welcome", "content": "Welcome to the WebSocket server!"}
    await websocket.send(json.dumps(initial_message))
    
    client = setup_chatbot()
    if client is None:
        await websocket.send(json.dumps({"type": "error", "content": "Chatbot setup failed."}))
        return

    try:
        async for message in websocket:
            response = await handle_message(websocket, message, client)
            if response == "exit":
                break
            if response:
                await websocket.send(response)
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        print("Client disconnected")

# Start WebSocket server
async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
