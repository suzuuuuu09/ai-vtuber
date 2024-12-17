from dotenv import load_dotenv
import os
import json
import websocket

load_dotenv()

# WebSocketの接続設定
port = os.getenv("OBS_WEBSOCKET_PORT", "4455")  # ポートが指定されていない場合はデフォルト値
host = f"ws://localhost:{port}"  # OBS WebSocketのURL
password = os.getenv("OBS_WEBSOCKET_PASS", "")  # OBS WebSocketのパスワード

# テキストソースの名前と変更したいテキスト
source_name = "reply_text"  # OBSで設定しているテキストソースの名前
new_text = "新しいテキスト内容"

# WebSocketのメッセージ構造
def on_open(ws):
    print("Connected to OBS WebSocket")
    # 認証メッセージ
    auth_message = {
        "request-type": "GetAuthRequired",
        "message-id": "1"
    }
    ws.send(json.dumps(auth_message))

def on_message(ws, message):
    message = json.loads(message)
    if message.get("message-id") == "1" and message["authRequired"]:
        print("Authentication is required.")
        auth_payload = {
            "request-type": "Authenticate",
            "message-id": "2",
            "auth": password
        }
        ws.send(json.dumps(auth_payload))
    elif message.get("message-id") == "2" and "status" in message:
        if message["status"] == "ok":
            print("Authenticated successfully.")
            # 認証成功後にテキスト変更リクエストを送信
            change_text_message = {
                "request-type": "SetSourceSettings",
                "sourceName": source_name,
                "sourceSettings": {"text": new_text},
                "message-id": "3"
            }
            ws.send(json.dumps(change_text_message))
        else:
            print("Authentication failed.")
    elif message.get("message-id") == "3":
        # テキスト変更リクエストのレスポンス
        if message["status"] == "ok":
            print("Text updated successfully.")
        else:
            print("Failed to update text.")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Closed connection")

# WebSocket接続
ws = websocket.WebSocketApp(
    host,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

# WebSocket接続開始
ws.run_forever()
