import os
from time import sleep
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# YouTube Data APIキー（ここに取得したAPIキーを記述）
API_KEY = os.getenv("GOOGLE_API_KEY")

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_live_chat_id(video_id):
    response = youtube.videos().list(
        part='liveStreamingDetails',
        id=video_id
    ).execute()

    items = response.get('items', [])
    if not items:
        print(f"動画ID {video_id} のライブチャットが見つかりません。")
        return None

    live_details = items[0].get('liveStreamingDetails', {})
    return live_details.get('activeLiveChatId')

def get_live_chat_messages(live_chat_id):
    response = youtube.liveChatMessages().list(
        liveChatId=live_chat_id,
        part='snippet,authorDetails'
    ).execute()

    return response.get('items', [])

def main(video_id):
    # ライブチャットIDを取得
    live_chat_id = get_live_chat_id(video_id)
    if not live_chat_id:
        return

    print(f"ライブチャットID: {live_chat_id}")

    # リアルタイムでライブチャットのコメントを取得
    while True:
        try:
            messages = get_live_chat_messages(live_chat_id)
            for message in messages:
                author = message['authorDetails']['displayName']
                text = message['snippet']['displayMessage']
                print(f"{author}: {text}")

            # 2秒待機してから再取得
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