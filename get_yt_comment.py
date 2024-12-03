import os
import requests
from time import sleep
from dotenv import load_dotenv

load_dotenv()

# YouTube Data APIキー（.envファイルから取得）
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GOOGLE_API_URL = "https://www.googleapis.com/youtube/v3"

def get_live_chat_id(video_id):
    url = f"{GOOGLE_API_URL}/videos"
    params = {
        "part": "liveStreamingDetails",
        "id": video_id,
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"エラー: {response.status_code}, 内容: {response.text}")
        return None

    data = response.json()
    items = data.get('items', [])
    if not items:
        print(f"動画ID {video_id} のライブチャットが見つかりません。")
        return None

    live_details = items[0].get('liveStreamingDetails', {})
    return live_details.get('activeLiveChatId')

def get_live_chat_messages(live_chat_id):
    url = f"{GOOGLE_API_URL}/liveChat/messages"
    params = {
        "liveChatId": live_chat_id,
        "part": "snippet,authorDetails",
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"エラー: {response.status_code}, 内容: {response.text}")
        return []

    data = response.json()
    return data.get('items', [])

def main(video_id):
    live_chat_id = get_live_chat_id(video_id)
    if not live_chat_id:
        return

    print(f"ライブチャットID: {live_chat_id}")

    diff_message = {}
    prev_diff_message = {}
    while True:
        try:
            messages = get_live_chat_messages(live_chat_id)
            for message in messages:
                message_id = message['id']
                if message_id not in diff_message:
                    user_name = message['authorDetails']['displayName']
                    comment = message['snippet']['displayMessage']
                    diff_message[message_id] = [user_name, comment]
                    # print(f"{user_name}: {comment}")
            if diff_message is not prev_diff_message:
                prev_diff_message = diff_message.copy()
                diff_message = {}
            
            print(diff_message)
# TODO: コメントを取得する
            sleep(5)
        except KeyboardInterrupt:
            print("プログラムが中断されました。")
            break
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            break

if __name__ == '__main__':
    video_id = input("ビデオIDを入力してください: ")
    main(video_id)