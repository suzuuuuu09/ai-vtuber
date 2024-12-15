import re
from urllib.parse import urlparse, parse_qs
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

def extract_channel_id(embed_url):
    """
    埋め込みリンクからチャンネルIDを抽出する
    """
    parsed_url = urlparse(embed_url)
    if "/embed/live_stream" in parsed_url.path:
        query_params = parse_qs(parsed_url.query)
        channel_id = query_params.get("channel", [None])[0]
        return channel_id
    return None

def get_live_video_id(api_key, channel_id):
    """
    チャンネルIDを基に現在ライブ中の動画IDを取得する
    """
    url = f"https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "id",
        "channelId": channel_id,
        "eventType": "live",  # 現在ライブ中の動画を対象
        "type": "video",
        "key": api_key,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            video_id = data["items"][0]["id"]["videoId"]
            return video_id
        else:
            return None  # ライブが見つからない場合
    else:
        print("APIエラー:", response.status_code, response.text)
        return None

if __name__ == "__main__":
    # 埋め込みリンク
    embed_url = "https://www.youtube.com/embed/live_stream?channel=UCdAHaWcKdpbT5XkN2Er6BUQ"

    # 埋め込みリンクからチャンネルIDを抽出
    channel_id = extract_channel_id(embed_url)
    if channel_id:
        print("チャンネルID:", channel_id)
        # チャンネルIDを基にライブ動画IDを取得
        video_id = get_live_video_id(API_KEY, channel_id)
        if video_id:
            print("現在のライブ動画ID:", video_id)
            print(f"動画リンク: https://www.youtube.com/watch?v={video_id}")
        else:
            print("現在ライブ配信中の動画は見つかりませんでした。")
    else:
        print("埋め込みリンクからチャンネルIDを取得できませんでした。")
