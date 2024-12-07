import os
import requests
import json
from time import sleep
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_API_URL = "https://www.googleapis.com/youtube/v3"

class YoutubeLiveChat:
    def __init__(self, video_id, api_key=GOOGLE_API_KEY, api_url=GOOGLE_API_URL):
        self.video_id = video_id
        self.api_key = api_key
        self.api_url = api_url
        self.prev_message = None

    def get_live_chat_id(self):
        url = f"{self.api_url}/videos"
        params = {
            "key": self.api_key,
            "part": "liveStreamingDetails",
            "id": self.video_id,
            "maxResults": 10,
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"エラー: {response.status_code}, 内容: {response.text}")
            return None

        data = response.json()
        items = data.get("items", [])
        if not items:
            print(f"動画ID {self.video_id} のライブチャットが見つかりません。")
            return None

        live_details = items[0].get("liveStreamingDetails", {})
        return live_details.get("activeLiveChatId")

    def get_live_chat_messages(self, live_chat_id):
        url = f"{self.api_url}/liveChat/messages"
        params = {
            "key": self.api_key,
            "liveChatId": live_chat_id,
            "part": "snippet,authorDetails",
            "maxResults": 10,
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"エラー: {response.status_code}, 内容: {response.text}")
            return []

        data = response.json()
        return data.get("items", []) or []

    def get_message(self):
        live_chat_id = self.get_live_chat_id()
        if not live_chat_id:
            return []

        try:
            messages = self.get_live_chat_messages(live_chat_id)
            new_messages = []

            for message in messages:
                message_id = message["id"]
                user_name = message["authorDetails"]["displayName"]
                user_id = message['authorDetails']['channelId']
                comment = message["snippet"]["displayMessage"]

                new_messages.append({
                    "message_id": message_id,
                    "data": [
                        {
                            "user_id": user_id,
                            "user_name": user_name,
                            "comment": comment
                        }
                    ]
                })

            return new_messages or []

        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return []

    def get_new_message(self, cur_messages):
        if not self.prev_message:
            return cur_messages

        last_chat_id = self.prev_message[-1]["message_id"]
        for i, item in enumerate(cur_messages):
            if item["message_id"] == last_chat_id:
                return cur_messages[i + 1:]

        return cur_messages


if __name__ == "__main__":
    video_id = "1TKWzt2B2Vo"
    yt_chat = YoutubeLiveChat(video_id)

    while True:
        cur_messages = yt_chat.get_message()
        new_messages = yt_chat.get_new_message(cur_messages)
        yt_chat.prev_message = cur_messages
        print(json.dumps(new_messages, indent=2, ensure_ascii=False))
        sleep(5)

# import os
# import requests
# import json
# from time import sleep
# from dotenv import load_dotenv

# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# GOOGLE_API_URL = "https://www.googleapis.com/youtube/v3"

# def get_live_chat_id(video_id):
#     url = f"{GOOGLE_API_URL}/videos"
#     params = {
#         "key": GOOGLE_API_KEY,
#         "part": "liveStreamingDetails",
#         "id": video_id,
#         "maxResults": 10,
#     }
#     response = requests.get(url, params=params)
#     if response.status_code != 200:
#         print(f"エラー: {response.status_code}, 内容: {response.text}")
#         return None

#     data = response.json()
#     items = data.get("items", [])
#     if not items:
#         print(f"動画ID {video_id} のライブチャットが見つかりません。")
#         return None

#     live_details = items[0].get("liveStreamingDetails", {})
#     return live_details.get("activeLiveChatId")

# def get_live_chat_messages(live_chat_id):
#     url = f"{GOOGLE_API_URL}/liveChat/messages"
#     params = {
#         "key": GOOGLE_API_KEY,
#         "liveChatId": live_chat_id,
#         "part": "snippet,authorDetails",
#         "maxResults": 10,
#     }
#     response = requests.get(url, params=params)
#     if response.status_code != 200:
#         print(f"エラー: {response.status_code}, 内容: {response.text}")
#         return []

#     data = response.json()
#     return data.get("items", []) or []

# def get_message(video_id):
#     live_chat_id = get_live_chat_id(video_id)
#     if not live_chat_id: return []
    
#     try:
#         messages = get_live_chat_messages(live_chat_id)
#         new_messages = []
        
#         for message in messages:
#             message_id = message["id"]
#             user_name = message["authorDetails"]["displayName"]
#             user_id = message['authorDetails']['channelId']
#             comment = message["snippet"]["displayMessage"]
            
#             new_messages.append({
#                 "message_id": message_id,
#                 "data": [
#                     {
#                         "user_id": user_id,
#                         "user_name": user_name,
#                         "comment": comment
#                     }
#                 ]
#             })
        
#         return new_messages or []
        
#     except Exception as e:
#         print(f"エラーが発生しました: {e}")
#         return []

# def get_new_message(cur_messages, prev_messages=None):
#     if not prev_messages:
#         return cur_messages
    
#     last_chat_id = prev_messages[-1]["message_id"]
#     for i, item in enumerate(cur_messages):
#         if item["message_id"] == last_chat_id:
#             return cur_messages[i + 1:]

#     return cur_messages

# class YoutubeLiveChat():
#     def __init__(self, video_id, 
#                  api_key = GOOGLE_API_KEY, 
#                  api_url = GOOGLE_API_URL):
#         self.video_id = video_id
#         self.api_key = api_key
#         self.api_url = api_url
#         self.prev_message = None

#     def get_live_chat_id(self):
#         url = f"{self.api_url}/videos"
#         params = {
#             "key": self.api_key,
#             "part": "liveStreamingDetails",
#             "id": self.video_id,
#             "maxResults": 10,
#         }
#         response = requests.get(url, params=params)
#         if response.status_code != 200:
#             # print(f"エラー: {response.status_code}, 内容: {response.text}")
#             return None

#         data = response.json()
#         items = data.get("items", [])
#         if not items:
#             messages = get_live_chat_messages(live_chat_id)
#             # print(f"動画ID {video_id} のライブチャットが見つかりません。")
#             return None

#         live_details = items[0].get("liveStreamingDetails", {})
#         return live_details.get("activeLiveChatId")
    
#     def get_message(self):
#         live_chat_id = get_live_chat_id(self.video_id)
#         if not live_chat_id: return []
        
#         try:
#             new_messages = []
            
#             for message in messages:
#                 message_id = message["id"]
#                 user_name = message["authorDetails"]["displayName"]
#                 user_id = message['authorDetails']['channelId']
#                 comment = message["snippet"]["displayMessage"]
                
#                 new_messages.append({
#                     "message_id": message_id,
#                     "data": [
#                         {
#                             "user_id": user_id,
#                             "user_name": user_name,
#                             "comment": comment
#                         }
#                     ]
#                 })
            
#             return new_messages or []
            
#         except Exception as e:
#             print(f"エラーが発生しました: {e}")
#             return []
        
#     def get_new_message(cur_messages, prev_messages=None):
#         if not prev_messages:
#             return cur_messages
        
#         last_chat_id = prev_messages[-1]["message_id"]
#         for i, item in enumerate(cur_messages):
#             if item["message_id"] == last_chat_id:
#                 return cur_messages[i + 1:]

#         return cur_messages

# if __name__ == "__main__":
#     video_id = "sX63uZnyZvY"
#     prev_message = None
#     while True:
#         cur_messages = get_message(video_id=video_id)
#         new_messages = get_new_message(cur_messages, prev_message)
#         prev_message = cur_messages
#         print(json.dumps(new_messages, indent=2, ensure_ascii=False))
#         sleep(5)
