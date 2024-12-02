import requests, os
from dotenv import load_dotenv

load_dotenv()

def get_access_token(client_id, client_secret):
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    response.raise_for_status()  # エラーがあれば例外を投げる
    return response.json()["access_token"]

def get_channel_id(username, client_id, access_token):
    url = "https://api.twitch.tv/helix/users"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}"  # 必須
    }
    params = {"login": username}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["data"][0]["id"]


access_token = get_access_token(client_id, client_secret)
print("Access Token:", access_token)

username = "fps_shaka"  # 配信者のTwitchユーザー名
client_id = os.getenv("TWITCH_CLIENT_ID")
access_token = os.getenv("TWITCH_ACCESS_TOKEN")
channel_id = get_channel_id(username, client_id, access_token)
print("Channel ID:", channel_id)