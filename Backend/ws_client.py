import websocket

def on_message(ws, message):
    print(f"Received: {message}")
    
def on_error(ws, error):
    print(f"Error: {error}")
    
def on_close(ws):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket opened")
    ws.send("Hello, server!")   

def send_message(ws, message):
    ws.send(message)

def start_ws():
    ws = websocket.WebSocketApp(
        "ws://localhost:8765",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()

# Only run the WebSocket if this script is executed directly
if __name__ == "__main__":
    start_ws()
