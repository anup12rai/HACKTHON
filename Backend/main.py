import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

async def main():
    start_server = await websockets.serve(echo, "localhost", 8765)
    print("Starting")
    await start_server.wait_closed()

# Ensure an event loop is running
if __name__ == "__main__":
    asyncio.run(main())