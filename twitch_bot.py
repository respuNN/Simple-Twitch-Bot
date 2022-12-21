import asyncio
import json
import requests
import websockets
from config import *

# Set up a WebSocket connection to the Twitch API
async def connect():
    url = f"wss://pubsub-edge.twitch.tv"
    async with websockets.connect(url) as websocket:
        # Listen for subscription events on the channel
        await websocket.send(json.dumps({
            "type": "LISTEN",
            "nonce": "subscribe-example",
            "data": {
                "topics": [f"channel-subscribe-events-v1.{CHANNEL_ID}"],
                "auth_token": ACCESS_TOKEN
            }
        }))

        while True:
            response = json.loads(await websocket.recv())
            # Check if the message is a subscription event
            if "subscription" in response["data"]:
                # Send a message to the channel
                send_message("Thank you for subscribing!")

# Send a message to the channel
def send_message(message):
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "channel_id": CHANNEL_ID,
        "message": message
    }
    requests.post("https://api.twitch.tv/helix/channels/broadcast/commercial", headers=headers, json=data)

# Run the bot
asyncio.get_event_loop().run_until_complete(connect())