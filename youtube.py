import requests, os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_API_URL = "https://www.googleapis.com/youtube/v3/"
video_id = "Soy4jGPHr3g"

# params = {
#     'key': GOOGLE_API_KEY,
#     'part': 'snippet',
#     'videoId': video_id,
#     'order': 'relevance',
#     'textFormat': 'plaintext',
#     'maxResults': 100,
# }

# if next_page_token is not None:
#     params['pageToken'] = next_page_token
# response = requests.get(URL + 'commentThreads', params=params)
# resource = response.json()
def get_live_chat_id(video_id):
    url = f"{GOOGLE_API_URL}/videos"
    params = {
        "part": "liveStreamingDetails",
        "id": video_id,
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if 'items' in data and len(data['items']) > 0:
        live_chat_id = data['items'][0]['liveStreamingDetails'].get('activeLiveChatId')
        return live_chat_id
    else:
        print("ライブ配信の情報が見つかりませんでした。")
        return None
    
def get_comments(live_chat_id):
    url = f"{GOOGLE_API_URL}/liveChat/messages",
    params = {
        'liveChatId': live_chat_id,
        'part': 'snippet',
        'key': GOOGLE_API_KEY
    }
    
    comments = []
    next_page_token = None

    while True:
        if next_page_token:
            params['pageToken'] = next_page_token
        
        response = requests.get(url, params=params)
        data = response.json()

        for item in data['items']:
            comment = item['snippet']['displayMessage']
            author = item['snippet']['authorDisplayName']
            comments.append((author, comment))
            print(f'{author}: {comment}')

        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break

    return comments

live_chat_id = get_live_chat_id(video_id)

if live_chat_id:
    print("取得")
    comments = get_comments(live_chat_id)
    print(f"\n{len(comments)}件")