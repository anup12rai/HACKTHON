import asyncio
import websockets

# Function to handle incoming WebSocket messages
async def handle_connection(websocket, path=None):
    async for message in websocket:
        print(f"Received message: {message}")
        # You can add any response logic here if needed
        await websocket.send(f"Message received: {message}")

# Start WebSocket server on port 8765
async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future() 

# Run the WebSocket server
if __name__ == "__main__":
    asyncio.run(main())
