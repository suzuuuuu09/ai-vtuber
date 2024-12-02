import socket, os
from dotenv import load_dotenv

load_dotenv()

def connect_to_twitch_chat(username, oauth_token, channel):
    # Twitch IRCサーバーの情報
    server = "irc.chat.twitch.tv"
    port = 6667

    # ソケット接続を作成
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server, port))

    # Twitch IRCに認証情報を送信
    irc.send(f"PASS {oauth_token}\r\n".encode('utf-8'))
    irc.send(f"NICK {username}\r\n".encode('utf-8'))
    irc.send(f"JOIN #{channel}\r\n".encode('utf-8'))

    print(f"Connected to #{channel} chat")

    while True:
        try:
            # サーバーからのメッセージを受信
            response = irc.recv(2048).decode('utf-8')

            # PINGへの応答を送信（接続維持のため）
            if response.startswith("PING"):
                irc.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
            else:
                # チャットメッセージを表示
                print(response)
        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

TWITCH_SECRET_KEY = os.getenv("TWITCH_SECRET_KEY")

# 自分のTwitchアカウント情報
username = "suzuuuuu09"        # 自分のTwitchユーザー名
oauth_token = f"oauth:{TWITCH_SECRET_KEY}"  # Twitch OAuthトークン
channel = "fps_shaka"        # 監視するチャンネル名

connect_to_twitch_chat(username, oauth_token, channel)