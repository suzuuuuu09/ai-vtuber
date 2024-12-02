import requests, os
from dotenv import load_dotenv

load_dotenv()

# APIキーと動画IDを設定
API_KEY = os.getenv("GOOGLE_API_KEY")
VIDEO_ID = 'coYw-eVU0Ks'

# YouTube Data APIのURL
BASE_URL = 'https://www.googleapis.com/youtube/v3'

# 動画IDからliveChatIdを取得
def get_live_chat_id(video_id):
    url = f'{BASE_URL}/videos'
    params = {
        'part': 'liveStreamingDetails',
        'id': video_id,
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if 'items' in data and len(data['items']) > 0:
        live_chat_id = data['items'][0]['liveStreamingDetails'].get('activeLiveChatId')
        return live_chat_id
    else:
        print("ライブ配信の情報が見つかりませんでした。")
        return None

# liveChatIdからコメントを取得
def get_comments(live_chat_id):
    url = f'{BASE_URL}/liveChat/messages'
    params = {
        'liveChatId': live_chat_id,
        'part': 'snippet',
        'key': API_KEY
    }
    
    comments = []
    next_page_token = None

    while True:
        if next_page_token:
            params['pageToken'] = next_page_token
        
        response = requests.get(url, params=params)
        data = response.json()

        # コメントの取得
        for item in data['items']:
            comment = item['snippet']['displayMessage']
            author = item['authorDetails']['displayName']
            comments.append((author, comment))
            print(f'{author}: {comment}')
        
        # 次のページのトークンがある場合、続けて取得
        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break

    return comments

# ライブ配信IDからコメントを取得
live_chat_id = get_live_chat_id(VIDEO_ID)

if live_chat_id:
    print("ライブ配信のコメント取得を開始します...\n")
    comments = get_comments(live_chat_id)
    print(f"\n{len(comments)} 件のコメントを取得しました。")
else:
    print("ライブ配信のコメント取得に失敗しました。")
