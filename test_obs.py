import os
from obswebsocket import obsws, requests
from dotenv import load_dotenv
from time import sleep

load_dotenv()

host = "localhost"
port = os.getenv("OBS_WEBSOCKET_PORT")
password = os.getenv("OBS_WEBSOCKET_PASS")
ws = obsws(host, port, password)
ws.connect()
print("接続")

def set_text(text):
    try:
        scene_name = "AI-Vtuber"
        source_name = "reply_text"

        ws.call(requests.SetInputSettings(
            inputName=source_name,
            inputSettings={"text": text},
            overlay=False
        ))

        print(f"Applied: {text}")
    except Exception as e:
        print(f"Error: {e}")

set_text("てすと")

ws.disconnect()
print("websocket接続完了")